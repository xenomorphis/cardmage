#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import sys
from textwrap import wrap
import toml
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image


def cl_main() -> None:
    """Entrypoint of command line interface."""

    arg_parser = argparse.ArgumentParser(description='Cardmage open-source card builder')
    arg_parser.add_argument("path", nargs="*", help="Path to one or more card's root TOML file. Leave empty to build "
                                                    "all root files found in the card directory")
    arg_parser.add_argument("-l", "--languages", help="Render card translations", default=False, action="store_true")
    arg_parser.add_argument("-p", "--print", help="Render card in print quality", default=False, action="store_true")
    arg_parser.add_argument("-t", "--test", help="Use test settings", default=False, action="store_true")

    args = arg_parser.parse_args()

    global base_dir
    global blueprint
    global buildpath
    global distpath
    global settings

    build_no = 1

    if args.test:
        try:
            settings = toml.load(dir_path("../testdata/settings.toml"))
        except FileNotFoundError:
            print("The test settings file could not be loaded (file does not exist).")
            sys.exit(0)
    else:
        try:
            settings = toml.load(dir_path("./settings.toml"))
        except FileNotFoundError:
            print("The projects' settings file could not be loaded (file does not exist).")
            sys.exit(0)
        except toml.TomlDecodeError:
            print("The projects' settings file could not be loaded (wrong file format).")
            sys.exit(0)

    base_dir = settings['paths']['base']
    buildpath = os.path.join(base_dir, '_build/')
    distpath = os.path.join(base_dir, 'dist/')

    if not os.path.exists(buildpath) and args.languages:
        os.mkdir(buildpath)

    if not os.path.exists(distpath):
        os.mkdir(distpath)

    if len(args.path) == 0:
        args.path = os.listdir(base_dir + settings['paths']['cards'])

        if len(args.path) == 0:
            print("No definition files found inside the card directory; therefore nothing to do.")
            sys.exit(0)

    builds_total = len(args.path)

    for card in args.path:
        try:
            blueprint = toml.load(dir_path(base_dir + settings['paths']['cards'] + card))
            print("[" + str(build_no) + "/" + str(builds_total) + "] " + "Build '" +
                  resolve_meta_tags(blueprint['card']['code']) + "' started.")

            # 2. Load the necessary preset .toml files based on blueprint data (fonts, layouts)
            font = toml.load(dir_path(base_dir + settings['paths']['fonts'] + blueprint['card']['font'] + ".toml"))
            layout = toml.load(dir_path(base_dir + settings['paths']['layouts'] + blueprint['layout']['type'] + ".toml"))
            icons = toml.load(dir_path(base_dir + settings['paths']['icons'] + layout['icons']['set'] + ".toml"))

            template = Image(filename=dir_path(base_dir + settings['paths']['layouts'] + layout['template']['file']))

            if layout['image']['use_vertical']:
                if args.print:
                    card_image = Image(
                        filename=dir_path(base_dir + settings['paths']['images'] + blueprint['image']['source_vertical_hd']))
                else:
                    card_image = Image(
                        filename=dir_path(base_dir + settings['paths']['images'] + blueprint['image']['source_vertical']))
            else:
                if args.print:
                    card_image = Image(
                        filename=dir_path(base_dir + settings['paths']['images'] + blueprint['image']['source_hd']))
                else:
                    card_image = Image(
                        filename=dir_path(base_dir + settings['paths']['images'] + blueprint['image']['source']))

        except FileNotFoundError as error:
            print(error)
            print("  - Build '" + resolve_meta_tags(blueprint['card']['code']) + ".png' failed.")
            build_no += 1
            continue

        except toml.TomlDecodeError:
            print("  -" + card + ": Wrong file format...")
            build_no += 1
            continue

        else:
            # 3. Use wand to construct the final card (save intermediate files in _build)
            with Color(layout['template']['background']) as bg:
                current = Image(width=layout['template']['size'][0], height=layout['template']['size'][1], background=bg)

            with Drawing() as draw:
                hero = card_image.clone()
                layer = template.clone()
                draw.composite(operator='atop', left=layout['config']['image_zone'][0],
                               top=layout['config']['image_zone'][1], width=hero.width, height=hero.height, image=hero)
                draw.composite(operator='atop', left=0, top=0, width=layer.width, height=layer.height, image=layer)

                if args.languages:
                    current.save(filename=str(buildpath + resolve_meta_tags(blueprint['card']['code']) + '-base.png'))

                # 4. Use wand to place text onto card (save intermediate files in _build)
                draw.font = base_dir + settings['paths']['fonts'] + get_title_font_style(font, 'fontstyle')
                draw.font_size = get_title_font_style(font, 'fontsize')
                draw.fill_color = Color(get_title_font_style(font, 'fontcolor'))
                draw.text_alignment = get_title_font_style(font, 'textalign')

                if 'outline' in font['tags']['title']:
                    draw.stroke_color = Color(font['tags']['title']['outline']['color'])
                    draw.stroke_width = font['tags']['title']['outline']['width']

                offset_x = get_alignment_offset(draw.text_alignment, layout, 'title')
                draw.text(layout['config']['title_zone'][0] + offset_x, layout['config']['title_zone'][1], blueprint['title'])
                draw(current)

                for module in blueprint['modules']:
                    if module + '_zone' in layout['modules']:
                        render_card_content(blueprint['modules'][module], layout, font, icons['icons'], module, draw)

                    else:
                        print("  - NOTICE: Module '" + module + "' found, but the current layout specifies no rendering"
                                                                " zone for this module; skipping")
                        continue

                draw(current)

            # 5. Save image in dist
            if args.print:
                current.transform_colorspace('cmyk')
                current.save(filename=str(distpath + resolve_meta_tags(blueprint['card']['code']) + "-cmyk.tif"))
            else:
                current.save(filename=str(distpath + resolve_meta_tags(blueprint['card']['code']) + ".png"))

            print("  - Build '" + resolve_meta_tags(blueprint['card']['code']) + "' completed.")
            build_no += 1

    # 6. Remove _build and it's contents
    if args.languages:
        shutil.rmtree(buildpath)


def dir_path(string: str):
    """
    Checks file paths for existence before using them.

    Parameters
    ----------
        string : str
            The path to be checked

    Raises
    ------
        FileNotFoundError
            Raised if the given path does not exist
    """
    if os.path.exists(string):
        return string
    else:
        raise FileNotFoundError(string)


def get_alignment_offset(align: str, layout: dict, module: str) -> int:
    """Checks current text alignment and returns the corresponding x-axis offset"""
    if align == 'center':
        if module == 'title':
            return int(layout['config']['title_zone_dimensions'][0] / 2)
        else:
            return int(layout['modules'][module + '_zone_dimensions'][0] / 2)
    elif align == 'right':
        if module == 'title':
            return int(layout['config']['title_zone_dimensions'][0])
        else:
            return int(layout['modules'][module + '_zone_dimensions'][0])
    else:
        return 0


def get_title_font_style(styling: dict, attribute: str):
    """Checks title font settings and returns the desired value"""
    if attribute in styling['tags']['title']:
        if attribute == "fontstyle":
            return styling['config']['font_' + styling['tags']['title'][attribute]]
        else:
            return styling['tags']['title'][attribute]
    else:
        if attribute == "fontstyle":
            return styling['config']['font_normal']
        else:
            return styling['default'][attribute]


def get_zone_coordinates(zone: list, iteration: int) -> list:
    """Returns the current zone target coordinates"""
    if isinstance(zone[0], int):
        target = [zone[0], zone[1]]
    else:
        target = [zone[iteration][0], zone[iteration][1]]

    return target


def prepare_image(icon: Image, size: list, mode: int) -> Image:
    """
    Returns an icon as Image object and scales it, if necessary

    Parameters
    ----------
        icon : Image
            The raw icon file as a wand.Image object
        size : list
            A list containing the icon's target size [x, y]
        mode : int
            Defines if the icon shouldn't be scaled at all (0), only scaled down if it's too big (1)
            or scaled in both directions to match the target size as close as possible (2)

    Returns
    -------
        Image
            The processed wand.Image object
    """
    if mode > 0:
        scale_x = size[0] / icon.width
        scale_y = size[1] / icon.height

        if mode == 1:
            if scale_x <= scale_y and scale_x <= 1:
                icon.resize(int(icon.width * scale_x), int(icon.height * scale_x))
            elif scale_x > scale_y and scale_y <= 1:
                icon.resize(int(icon.width * scale_y), int(icon.height * scale_y))
        else:
            if scale_x <= scale_y:
                icon.resize(int(icon.width * scale_x), int(icon.height * scale_x))
            else:
                icon.resize(int(icon.width * scale_y), int(icon.height * scale_y))

    return icon


def render_card_content(data: dict, layout: dict, font: dict, icons: dict, module: str, draw: Drawing) -> None:
    """
    Renders a card's modules

    Parameters
    ----------
        data : dict
            The card data of the current module
        layout : dict
            The layout settings of the current card
        font : dict
            The default font settings
        icons : dict
            The current icon set
        module : str
            The name of the current module
        draw : Drawing
            A wand.Drawing object used for placing elements onto a card
    """
    target_coordinates = layout['modules'][module + '_zone']

    with Color('transparent') as bg:
        content_layer = Image(width=layout['modules'][module + '_zone_dimensions'][0],
                              height=layout['modules'][module + '_zone_dimensions'][1], background=bg)
        offset = [0, 0]

    with Drawing() as render:
        default_prio = ['image', 'prefix', 'condition', 'paragraph', 'list', 'icons', 'array']

        if 'content' in data:
            priorities = data['content']
        else:
            priorities = default_prio

        for ctype in priorities:
            # load default font settings
            render.font = base_dir + settings['paths']['fonts'] + font['config']['font_' + font['default']['fontstyle']]
            render.font_size = font['default']['fontsize']
            render.fill_color = Color(font['default']['fontcolor'])
            render.text_alignment = font['default']['textalign']

            if 'textdecoration' in font['default']:
                render.text_decoration = font['default']['textdecoration']
            else:
                render.text_decoration = 'no'

            # load module-specific font settings over defaults
            if module in font['modules']:
                if 'fontstyle' in font['modules'][module]:
                    render.font = base_dir + settings['paths']['fonts'] + font['config'][
                        'font_' + font['modules'][module]['fontstyle']]

                if 'fontsize' in font['modules'][module]:
                    render.font_size = font['modules'][module]['fontsize']

                if 'fontcolor' in font['modules'][module]:
                    render.fill_color = Color(font['modules'][module]['fontcolor'])

                if 'outline' in font['modules'][module]:
                    render.stroke_color = Color(font['modules'][module]['outline']['color'])
                    render.stroke_width = font['modules'][module]['outline']['width']

                if 'textalign' in font['modules'][module]:
                    render.text_alignment = font['modules'][module]['textalign']

                if 'textdecoration' in font['modules'][module]:
                    render.text_decoration = font['modules'][module]['textdecoration']

            # load tag-specific font settings over card-specific font settings over
            # module-specific font settings
            if ctype in data:
                if ctype in font['tags']:
                    tag_override = True
                else:
                    tag_override = False

                if tag_override and 'fontstyle' in font['tags'][ctype]:
                    render.font = base_dir + settings['paths']['fonts'] + font['config'][
                        'font_' + font['tags'][ctype]['fontstyle']]
                elif 'fontstyle' in data:
                    render.font = base_dir + settings['paths']['fonts'] + font['config']['font_' + data['fontstyle']]

                if tag_override and 'fontsize' in font['tags'][ctype]:
                    render.font_size = font['tags'][ctype]['fontsize']
                elif 'fontsize' in data:
                    render.font_size = data['fontsize']

                if tag_override and 'color' in font['tags'][ctype]:
                    render.fill_color = font['tags'][ctype]['fontcolor']
                elif 'fontcolor' in data:
                    render.fill_color = Color(data['fontcolor'])

                if tag_override and 'textalign' in font['tags'][ctype]:
                    render.text_alignment = font['tags'][ctype]['textalign']
                elif 'textalign' in data:
                    render.text_alignment = data['textalign']

                if tag_override and 'textdecoration' in font['tags'][ctype]:
                    render.text_decoration = font['tags'][ctype]['textdecoration']
                elif 'textdecoration' in data:
                    render.text_decoration = data['textdecoration']

                if 'outline' in data:
                    render.stroke_color = Color(data['outline']['color'])
                    render.stroke_width = data['outline']['width']

                space_offset = render.get_font_metrics(content_layer, ' ', True)

                if ctype == 'array':
                    iteration = 0
                    rendered = 0

                    if 'keys_as' in data:
                        keys_mode = data['keys_as']
                    else:
                        keys_mode = 'none'

                    if isinstance(target_coordinates[0], int) or len(target_coordinates) == 1:
                        targets = get_zone_coordinates(target_coordinates, iteration)

                        with Color('transparent') as bg:
                            content_layer = Image(width=layout['modules'][module + '_zone_dimensions'][0],
                                                  height=layout['modules'][module + '_zone_dimensions'][1],
                                                  background=bg)

                        with Drawing() as gfx:
                            gfx.font = render.font
                            gfx.font_size = render.font_size
                            gfx.fill_color = render.fill_color
                            gfx.text_alignment = render.text_alignment

                            if render.stroke_color:
                                gfx.stroke_color = render.stroke_color

                            if render.stroke_width:
                                gfx.stroke_width = render.stroke_width

                            text = ""

                            if offset[0] > 0 and gfx.text_alignment == 'left':
                                text += int(1 + offset[0] / space_offset.text_width) * ' '

                            for number in data[ctype]:
                                if number > 0:
                                    if rendered > 0:
                                        text += ", "

                                    if keys_mode == 'text':
                                        text += str(number) + " " + data['keys'][iteration]
                                    elif keys_mode == 'icons':
                                        text += str(number)

                                        try:
                                            icon_file = Image(
                                                filename=dir_path(base_dir + settings['paths']['icons'] +
                                                                  icons[data['keys'][iteration]]))
                                        except FileNotFoundError:
                                            print("  - NOTICE: Required icon file " + settings['paths']['icons'] +
                                                  icons[data['keys'][iteration]] + " not found. Skipping...")
                                            continue
                                        else:
                                            icon_layer = prepare_image(
                                                icon_file.clone(), [layout['modules'][module + '_zone_dimensions'][0],
                                                                    int(1.2 * gfx.font_size)], 1)
                                            text_offset = gfx.get_font_metrics(content_layer, text, True)
                                            draw.composite(operator='atop',
                                                           left=targets[0] + text_offset.text_width + 4,
                                                           top=targets[1] + text_offset.text_height - int(1.2 * gfx.font_size),
                                                           width=icon_layer.width, height=icon_layer.height,
                                                           image=icon_layer)

                                            text += int((icon_layer.width + 10) / space_offset.text_width) * ' '
                                    else:
                                        print("  - NOTICE: No 'keys_as' or 'keys' attribute found; "
                                              "using default 'keys_as = none'")
                                        text += str(number)

                                    rendered += 1

                                iteration += 1

                            offset[0] = get_alignment_offset(render.text_alignment, layout, module)

                            if keys_mode == 'icons':
                                render_text_multiline(text, content_layer, offset, gfx, mod=1.5)
                            else:
                                render_text_multiline(text, content_layer, offset, gfx)

                            gfx.draw(content_layer)

                        draw.composite(operator='atop', left=targets[0], top=targets[1], width=content_layer.width,
                                       height=content_layer.height, image=content_layer)

                    else:
                        offset[0] += get_alignment_offset(render.text_alignment, layout, module)

                        for number in data[ctype]:
                            targets = get_zone_coordinates(target_coordinates, rendered)

                            if number > 0:
                                with Color('transparent') as bg:
                                    content_layer = Image(width=layout['modules'][module + '_zone_dimensions'][0],
                                                          height=layout['modules'][module + '_zone_dimensions'][1],
                                                          background=bg)

                                with Drawing() as gfx:
                                    gfx.font = render.font
                                    gfx.font_size = render.font_size
                                    gfx.fill_color = render.fill_color
                                    gfx.text_alignment = render.text_alignment

                                    if render.stroke_color:
                                        gfx.stroke_color = render.stroke_color

                                    if render.stroke_width:
                                        gfx.stroke_width = render.stroke_width

                                    text = ""

                                    if keys_mode == 'text':
                                        text += str(number) + " " + data['keys'][iteration]
                                    elif keys_mode == 'icons':
                                        text += str(number)

                                        try:
                                            icon_file = Image(
                                                filename=dir_path(base_dir + settings['paths']['icons'] +
                                                                  icons[data['keys'][iteration]]))
                                        except FileNotFoundError:
                                            print("  - NOTICE: Required icon file " + settings['paths']['icons'] +
                                                  icons[data['keys'][iteration]] + " not found. Skipping...")
                                            continue
                                        else:
                                            icon_layer = prepare_image(
                                                icon_file.clone(), layout['modules'][module + '_zone_dimensions'], 0)
                                            draw.composite(operator='atop',
                                                           left=targets[0] + layout['modules'][module + '_zone_icon_offset'][0],
                                                           top=targets[1] + layout['modules'][module + '_zone_icon_offset'][1],
                                                           width=icon_layer.width, height=icon_layer.height,
                                                           image=icon_layer)
                                    else:
                                        print("  - NOTICE: No 'keys_as' or 'keys' attribute found; "
                                              "using default 'keys_as = none'")
                                        text += str(number)

                                    gfx.text(int(offset[0]), int(render.font_size + offset[1]), text)
                                    gfx.draw(content_layer)

                                if rendered < len(target_coordinates) - 1:
                                    rendered += 1

                                draw.composite(operator='atop', left=targets[0], top=targets[1],
                                               width=content_layer.width, height=content_layer.height,
                                               image=content_layer)

                            iteration += 1

                elif ctype == 'icons':
                    iteration = 0
                    max_height = 0

                    if isinstance(target_coordinates[0], int) or len(target_coordinates) == 1:
                        targets = get_zone_coordinates(target_coordinates, iteration)

                        for icon in data[ctype]:
                            try:
                                icon_file = Image(
                                    filename=dir_path(base_dir + settings['paths']['icons'] + icons[icon]))
                            except FileNotFoundError:
                                print("  - NOTICE: Required icon file " + settings['paths']['icons'] + icons[icon] +
                                      " not found. Skipping...")
                                continue
                            else:
                                icon_layer = prepare_image(
                                    icon_file.clone(), layout['modules'][module + '_zone_dimensions'], 1)
                                draw.composite(operator='atop', left=targets[0] + offset[0], top=targets[1] + offset[1],
                                               width=icon_layer.width, height=icon_layer.height, image=icon_layer)

                                if icon_layer.height > max_height:
                                    max_height = icon_layer.height

                                if (offset[0] + icon_layer.width + 5) > layout['modules'][module + '_zone_dimensions'][0]:
                                    offset[0] = 0
                                    offset[1] += max_height + 5
                                    max_height = icon_layer.height
                                else:
                                    offset[0] += icon_layer.width + 5

                    else:
                        for icon in data[ctype]:
                            if iteration < len(target_coordinates):
                                targets = get_zone_coordinates(target_coordinates, iteration)

                                try:
                                    icon_file = Image(
                                        filename=dir_path(base_dir + settings['paths']['icons'] + icons[icon]))
                                except FileNotFoundError:
                                    print("  - NOTICE: Required icon file " + settings['paths']['icons'] + icons[icon] +
                                          " not found. Skipping...")
                                    iteration += 1
                                    continue
                                else:
                                    icon_layer = prepare_image(
                                        icon_file.clone(), layout['modules'][module + '_zone_dimensions'], 1)
                                    draw.composite(operator='atop', left=targets[0], top=targets[1],
                                                   width=icon_layer.width, height=icon_layer.height, image=icon_layer)

                                iteration += 1

                elif ctype == 'list':
                    for element in data[ctype]:
                        content = resolve_meta_tags(element)
                        content = word_wrap(content_layer, render, content,
                                            content_layer.width - int(1 * render.font_size),
                                            content_layer.height - offset[1])
                        metrics = render.get_font_metrics(content_layer, content, True)
                        render.text(int(offset[0]), int(render.font_size + offset[1]), '–')
                        render.text(int(1 * render.font_size + offset[0]), int(render.font_size + offset[1]), content)
                        offset[1] += metrics.text_height + int(render.font_size * 0.25)

                    render.draw(content_layer)

                elif ctype == 'image':
                    try:
                        image = Image(filename=dir_path(base_dir + settings['paths']['images'] + data[ctype]))
                    except FileNotFoundError:
                        print("  - NOTICE: Required image file " + settings['paths']['images'] + data[ctype] +
                              " not found. Skipping...")
                        continue
                    else:
                        render.composite(operator='atop', left=0, top=0, width=image.width, height=image.height, image=image)
                        render.draw(content_layer)

                else:
                    if ctype in default_prio:
                        raw_content = data[ctype]
                    else:
                        try:
                            str_index = data['paragraph']['alias'].index(ctype)
                        except ValueError:
                            print("  - NOTICE: Couldn't find a paragraph named " + ctype + ". Skipping...")
                            continue
                        else:
                            raw_content = data['paragraph']['text'][str_index]

                    offset[0] += get_alignment_offset(render.text_alignment, layout, module)
                    content = resolve_meta_tags(raw_content)
                    new_offset = render_text_multiline(content, content_layer, offset, render)

                    if ctype == 'prefix':
                        offset[0] += new_offset[0] + int(render.font_size * 0.25)
                    else:
                        offset[0] = 0
                        offset[1] += new_offset[1] + int(render.font_size * 0.25)

                    render.draw(content_layer)

                if ctype != 'array':
                    draw.composite(operator='atop', left=target_coordinates[0], top=target_coordinates[1],
                                   width=content_layer.width, height=content_layer.height, image=content_layer)

            else:
                continue


def render_text_multiline(content: str, layer: Image, offset: list, render: Drawing, mod=1.0) -> list:
    """
    Renders text depending on available space and current horizontal offsets.

    Parameters
    ----------
        content : str
            The text to be rendered
        layer : Image
            A wand.Image object used as a carrier for the rendering process of the current module
        offset : list
            Contains the current rendering offset based on the modules base coordinates [x, y]
        render : Drawing
            A wand.Drawing object used for placing elements onto an Image object
        mod : float
            Optional modifier used for increasing the 'Mode 2' threshold if the 'content' is likely to contain a
            lot of spaces

    Returns
    -------
        list
            A list containing the new offset values resulting from the text rendering
    """
    new_offset = [0, 0]

    # estimated amount of possible characters that can be rendered in the current rendering zone
    chars_line = int(layer.width / (0.75 * render.font_size)) * mod
    lines_max = int((layer.height - offset[1]) / (1.2 * render.font_size))
    chars_max = (lines_max - 1) * chars_line

    if offset[0] == 0 or render.text_alignment != 'left' or len(content) > chars_max:
        if offset[0] > 0 and render.text_alignment == 'left':
            offset[0] = 0
            offset[1] += new_offset[1] + int(render.font_size * 0.25)

        content = word_wrap(layer, render, content, layer.width, layer.height - offset[1])
        render.text(int(offset[0]), int(render.font_size + offset[1]), content)

        if '\n' in content:
            metrics = render.get_font_metrics(layer, content, True)
        else:
            metrics = render.get_font_metrics(layer, content, False)

        new_offset = [metrics.text_width, metrics.text_height]

    else:
        # Fill up the prefixed line first
        content_fl = word_wrap(layer, render, content, layer.width - offset[0], layer.height - offset[1])
        content_fl = content_fl.partition('\n')[0]
        render.text(int(offset[0]), int(render.font_size + offset[1]), content_fl)
        metrics = render.get_font_metrics(layer, content_fl, False)

        if len(content) > len(content_fl):
            # render what's left normally and calculate the height of both text blocks
            content_rest = word_wrap(layer, render, content[len(content_fl):].strip(), layer.width,
                                     layer.height - offset[1])
            render.text(0, int(2.2 * render.font_size + offset[1]), content_rest)

            if '\n' in content_rest:
                metrics_rest = render.get_font_metrics(layer, content_rest, False)
            else:
                metrics_rest = render.get_font_metrics(layer, content_rest, False)

            new_offset = [0, metrics.text_height + metrics_rest.text_height]

    return new_offset


def resolve_meta_tags(string: str) -> str:
    """
    Resolves and replaces meta_tags

    Parameters
    ----------
        string : str
            The text to be checked for meta tags

    Returns
    -------
        str
            Text with replaced meta tags
    """
    meta_tags = ['{', '}']
    has_meta_tags = all([char in string for char in meta_tags])

    if has_meta_tags:
        content_parts = re.findall(r'\{.*?}', string)

        for tag in content_parts:
            meta_key = tag.replace('{', '').replace('}', '')

            if meta_key in blueprint['meta']:
                string = string.replace(tag, blueprint['meta'][meta_key])
            elif meta_key == 'title':
                string = string.replace(tag, blueprint['title'])

    return string


def word_wrap(image: Image, ctx: Drawing, text: str, roi_width: int, roi_height: int):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    iteration_attempts = 30

    def eval_metrics(txt: str):
        """Calculates width/height of text."""
        if '\n' in txt:
            metrics = ctx.get_font_metrics(image, txt, True)
        else:
            metrics = ctx.get_font_metrics(image, txt, False)

        return (metrics.text_width, metrics.text_height)

    while ctx.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(mutable_message)

        if height > roi_height:
            ctx.font_size -= 0.5  # Reduce font size
            mutable_message = text  # Restore original text
        elif width > roi_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                mutable_message = '\n'.join(wrap(mutable_message, columns))
                wrapped_width, _ = eval_metrics(mutable_message)

                if wrapped_width <= roi_width:
                    break

            if columns < 1:
                ctx.font_size -= 0.5  # Reduce font size
                mutable_message = text  # Restore original text

        else:
            break

    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)

    return mutable_message


if __name__ == "__main__":
    cl_main()
