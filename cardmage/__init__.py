#!/usr/bin/env python3

import argparse
import os
import re
import shutil
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

                if 'color' in font['tags']['title']:
                    draw.fill_color = Color(font['tags']['title']['color'])
                else:
                    draw.fill_color = Color(font['default']['color'])

                if 'textalign' in font['tags']['title']:
                    draw.text_alignment = font['tags']['title']['textalign']
                else:
                    draw.text_alignment = font['default']['textalign']

                if 'outline' in font['tags']['title']:
                    draw.stroke_color = Color(font['tags']['title']['outline']['color'])
                    draw.stroke_width = font['tags']['title']['outline']['width']

                draw.text(layout['config']['title_zone'][0], layout['config']['title_zone'][1], blueprint['title'])
                draw(current)
                uts = str(int(time.time()))
                current.save(filename=buildpath + uts + "-template.png")

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
                            textlayer = Image(width=layout['modules'][module + '_zone_dimensions'][0],
                                              height=layout['modules'][module + '_zone_dimensions'][1], background=bg)
                            offset = [0, 0]

                        with Drawing() as render:
                            priorities = ['image', 'prefix', 'condition', 'paragraph', 'list', 'array']

                            for ctype in priorities:
                                # load default font settings
                                render.font = base_dir + settings['paths']['fonts'] + font['config']['font_normal']
                                render.font_size = font['default']['fontsize']
                                render.fill_color = Color(font['default']['color'])
                                render.text_alignment = font['default']['textalign']

                                # load module-specific font settings over defaults
                                if module in font['modules']:
                                    if 'fontstyle' in font['modules'][module]:
                                        render.font = base_dir + settings['paths']['fonts'] + font['config'][
                                            'font_' + font['modules'][module]['fontstyle']]

                                    if 'fontsize' in font['modules'][module]:
                                        render.font_size = font['modules'][module]['fontsize']

                                    if 'color' in font['modules'][module]:
                                        render.fill_color = Color(font['modules'][module]['color'])

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
                                        render.fill_color = font['tags'][ctype]['color']
                                    elif 'color' in blueprint['modules'][module]:
                                        render.fill_color = Color(blueprint['modules'][module]['color'])

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
                                            if targets > 1:
                                                if number > 0:
                                                    with Color('transparent') as bg:
                                                        textlayer = Image(
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
                                                        gfx.draw(textlayer)
                                                        uts = str(int(time.time()))
                                                        fname = buildpath + uts + "-" + module + str(iteration) + ".png"
                                                        textlayer.save(filename=fname)

                                                    draw.composite(operator='atop', left=target_coordinates[iteration][0],
                                                                   top=target_coordinates[iteration][1],
                                                                   width=textlayer.width, height=textlayer.height,
                                                                   image=textlayer)

                                                    iteration += 1

                                    elif ctype == 'list':
                                        pass
                                    elif ctype == 'image':
                                        pass
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

                                        render.text(int(0 + offset[0]), int(render.font_size + offset[1]), content)
                                        # print(render.get_font_metrics(textlayer, blueprint['modules'][module][ctype], True))

                                        render.draw(textlayer)
                                        uts = str(int(time.time()))
                                        fname = buildpath + uts + "-" + module + ".png"
                                        textlayer.save(filename=fname)
                                        draw.composite(operator='atop', left=target_coordinates[0],
                                                       top=target_coordinates[1],
                                                       width=textlayer.width, height=textlayer.height, image=textlayer)
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


if __name__ == "__main__":
    cl_main()
