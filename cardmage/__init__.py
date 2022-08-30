#!/usr/bin/env python3

import argparse
import os
import re
import shutil
from textwrap import wrap
import time
import toml
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image, COMPOSITE_OPERATORS


def cl_main() -> None:
    """
    Entrypoint of command line interface.
    """

    arg_parser = argparse.ArgumentParser(description='Cardmage open-source card builder')
    arg_parser.add_argument("path", nargs="+", help="Path to the card's root TOML file")
    arg_parser.add_argument("-p", "--print", help="Render card in print quality", default=False, action="store_true")
    arg_parser.add_argument("-t", "--test", help="Use test settings", default=False, action="store_true")

    args = arg_parser.parse_args()

    blueprint = dict()

    if args.test:
        settings = toml.load(dir_path("../testdata/settings.toml"))
    else:
        settings = toml.load(dir_path("./settings.toml"))

    base_dir = settings['paths']['base']
    buildpath = os.path.join(base_dir, '_build/')
    distpath = os.path.join(base_dir, 'dist/')

    meta_tags = ['{', '}']

    if not os.path.exists(buildpath):
        os.mkdir(buildpath)

    if not os.path.exists(distpath):
        os.mkdir(distpath)

    for card in args.path:
        try:
            blueprint = toml.load(dir_path(base_dir + settings['paths']['cards'] + card))
            print("Build '" + blueprint['meta']['edition'] + "-" + blueprint['meta']['id'] + ".png' started.")

            # 2. Load the necessary preset .toml files based on blueprint data (fonts, layouts)
            font = toml.load(dir_path(base_dir + settings['paths']['fonts'] + blueprint['card']['font'] + ".toml"))
            layout = toml.load(dir_path(base_dir + settings['paths']['layouts'] + blueprint['layout']['type'] + ".toml"))

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
            print("- Build '" + blueprint['meta']['edition'] + "-" + blueprint['meta']['id'] + ".png' failed.")
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

                # 4. Use wand to place text onto card (save intermediate files in _build)
                if 'fontstyle' in font['tags']['title']:
                    draw.font = base_dir + settings['paths']['fonts'] + font['config']['font_' + font['tags']['title']['fontstyle']]
                else:
                    draw.font = base_dir + settings['paths']['fonts'] + font['config']['font_normal']

                if 'fontsize' in font['tags']['title']:
                    draw.font_size = font['tags']['title']['fontsize']
                else:
                    draw.font_size = font['default']['fontsize']

                if 'fontcolor' in font['tags']['title']:
                    draw.fill_color = Color(font['tags']['title']['fontcolor'])
                else:
                    draw.fill_color = Color(font['default']['fontcolor'])

                if 'textalign' in font['tags']['title']:
                    draw.text_alignment = font['tags']['title']['textalign']
                else:
                    draw.text_alignment = font['default']['textalign']

                if 'outline' in font['tags']['title']:
                    draw.stroke_color = Color(font['tags']['title']['outline']['color'])
                    draw.stroke_width = font['tags']['title']['outline']['width']

                draw.text(layout['config']['title_zone'][0], layout['config']['title_zone'][1], blueprint['title'])
                draw(current)
                current.save(filename=get_temp_name(buildpath, 'template'))

                for module in blueprint['modules']:
                    if module + '_zone' in layout['modules']:
                        target_coordinates = layout['modules'][module + '_zone']

                        if isinstance(target_coordinates[0], int):
                            targets = 1
                        else:
                            targets = len(target_coordinates)

                        # print(module)
                        # print(targets)

                        with Color('transparent') as bg:
                            content_layer = Image(width=layout['modules'][module + '_zone_dimensions'][0],
                                              height=layout['modules'][module + '_zone_dimensions'][1], background=bg)
                            offset = [0, 0]

                        with Drawing() as render:
                            if 'content' in blueprint['modules'][module]:
                                priorities = blueprint['modules'][module]['content']
                            else:
                                priorities = ['image', 'prefix', 'condition', 'paragraph', 'list', 'array']

                            for ctype in priorities:
                                # load default font settings
                                render.font = base_dir + settings['paths']['fonts'] + font['config']['font_normal']
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
                                if ctype in blueprint['modules'][module]:
                                    if ctype in font['tags']:
                                        tag_override = True
                                    else:
                                        tag_override = False

                                    if tag_override and 'fontstyle' in font['tags'][ctype]:
                                        render.font = base_dir + settings['paths']['fonts'] + font['config'][
                                            'font_' + font['tags'][ctype]['fontstyle']]
                                    elif 'fontstyle' in blueprint['modules'][module]:
                                        render.font = base_dir + settings['paths']['fonts'] + font['config'][
                                            'font_' + blueprint['modules'][module]['fontstyle']]

                                    if tag_override and 'fontsize' in font['tags'][ctype]:
                                        render.font_size = font['tags'][ctype]['fontsize']
                                    elif 'fontsize' in blueprint['modules'][module]:
                                        render.font_size = blueprint['modules'][module]['fontsize']

                                    if tag_override and 'color' in font['tags'][ctype]:
                                        render.fill_color = font['tags'][ctype]['fontcolor']
                                    elif 'fontcolor' in blueprint['modules'][module]:
                                        render.fill_color = Color(blueprint['modules'][module]['fontcolor'])

                                    if tag_override and 'textalign' in font['tags'][ctype]:
                                        render.text_alignment = font['tags'][ctype]['textalign']
                                    elif 'textalign' in blueprint['modules'][module]:
                                        render.text_alignment = blueprint['modules'][module]['textalign']

                                    if tag_override and 'textdecoration' in font['tags'][ctype]:
                                        render.text_decoration = font['tags'][ctype]['textdecoration']
                                    elif 'textdecoration' in blueprint['modules'][module]:
                                        render.text_decoration = blueprint['modules'][module]['textdecoration']

                                    if 'outline' in blueprint['modules'][module]:
                                        render.stroke_color = Color(blueprint['modules'][module]['outline']['color'])
                                        render.stroke_width = blueprint['modules'][module]['outline']['width']

                                    if ctype == 'array':
                                        iteration = 0

                                        for number in blueprint['modules'][module][ctype]:
                                            if number > 0:
                                                with Color('transparent') as bg:
                                                    content_layer = Image(
                                                        width=layout['modules'][module + '_zone_dimensions'][0],
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

                                                    if render.text_alignment == 'center':
                                                        offset[0] = int(
                                                            layout['modules'][module + '_zone_dimensions'][0] / 2)

                                                    gfx.text(int(0 + offset[0]), int(render.font_size + offset[1]),
                                                             str(number))
                                                    gfx.draw(content_layer)
                                                    content_layer.save(filename=get_temp_name(
                                                        buildpath, module + str(iteration)))

                                                    if isinstance(target_coordinates[0], int):
                                                        draw.composite(operator='atop',
                                                                       left=target_coordinates[0],
                                                                       top=target_coordinates[1],
                                                                       width=content_layer.width,
                                                                       height=content_layer.height,
                                                                       image=content_layer)
                                                    else:
                                                        draw.composite(operator='atop',
                                                                       left=target_coordinates[iteration][0],
                                                                       top=target_coordinates[iteration][1],
                                                                       width=content_layer.width,
                                                                       height=content_layer.height,
                                                                       image=content_layer)

                                                        if iteration < targets - 1:
                                                            iteration += 1

                                    elif ctype == 'list':
                                        pass
                                    elif ctype == 'image':
                                        image = Image(filename=dir_path(base_dir + settings['paths']['images'] +
                                                                        blueprint['modules'][module][ctype]))
                                        render.composite(operator='atop', left=0, top=0, width=image.width,
                                                         height=image.height, image=image)
                                        render.draw(content_layer)
                                        content_layer.save(filename=get_temp_name(buildpath, module))
                                    else:
                                        # resolve and replace meta_tags
                                        content = blueprint['modules'][module][ctype]
                                        has_meta_tags = all([char in content for char in meta_tags])

                                        if has_meta_tags:
                                            content_parts = re.findall(r'\{.*?\}', content)

                                            for tag in content_parts:
                                                meta_key = tag.replace('{', '').replace('}', '')

                                                if meta_key in blueprint['meta']:
                                                    content = content.replace(tag, blueprint['meta'][meta_key])
                                                elif meta_key == 'title':
                                                    content = content.replace(tag, blueprint['title'])

                                        if render.text_alignment == 'center':
                                            offset[0] += int(layout['modules'][module + '_zone_dimensions'][0] / 2)

                                        content = word_wrap(content_layer, render, content, content_layer.width,
                                                            content_layer.height - offset[1])

                                        render.text(int(0 + offset[0]), int(render.font_size + offset[1]), content)
                                        metrics = render.get_font_metrics(content_layer, content, True)

                                        if ctype == 'prefix':
                                            offset[0] += metrics.text_width + int(render.font_size * 0.25)
                                        else:
                                            offset[1] += metrics.text_height + int(render.font_size * 0.25)

                                        render.draw(content_layer)
                                        content_layer.save(filename=get_temp_name(buildpath, module))

                                    if ctype != 'array':
                                        draw.composite(operator='atop', left=target_coordinates[0],
                                                       top=target_coordinates[1], width=content_layer.width,
                                                       height=content_layer.height, image=content_layer)

                                else:
                                    continue

                    else:
                        continue

                draw(current)

            # 5. Save image in dist
            current.save(filename=str(distpath + blueprint['meta']['edition'] + "-" + blueprint['meta']['id'] + ".png"))
            print("- Build '" + blueprint['meta']['edition'] + "-" + blueprint['meta']['id'] + ".png' completed.")

    # 6. Remove _build and it's contents
    shutil.rmtree(buildpath)


def dir_path(string):
    if os.path.exists(string):
        return string
    else:
        raise FileNotFoundError(string)


def get_temp_name(path, module) -> str:
    uts = str(int(time.time()))
    fname = path + uts + "-" + module + ".png"

    return fname


def word_wrap(image, ctx, text, roi_width, roi_height):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    iteration_attempts = 30

    def eval_metrics(txt):
        """Calculates width/height of text."""
        metrics = ctx.get_font_metrics(image, txt, True)
        return (metrics.text_width, metrics.text_height)

    while ctx.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(mutable_message)
        if height > roi_height:
            ctx.font_size -= 0.5  # Reduce pointsize
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
                ctx.font_size -= 0.5  # Reduce pointsize
                mutable_message = text  # Restore original text
        else:
            break
    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)
    return mutable_message


if __name__ == "__main__":
    cl_main()
