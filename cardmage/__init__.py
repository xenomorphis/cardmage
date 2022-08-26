#!/usr/bin/env python3

import argparse
import json
import os
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

    if not os.path.exists(buildpath):
        os.mkdir(buildpath)

    if not os.path.exists(distpath):
        os.mkdir(distpath)
    # working_dir = os.getcwd()

    for card in args.path:
        try:
            blueprint = toml.load(dir_path(base_dir + settings['paths']['cards'] + card))
            print("Build '" + blueprint['meta']['edition'] + "-" + blueprint['meta']['id'] + ".png' started.")

            # 2. Load the necessary preset .toml files based on blueprint data (fonts, layouts)
            font = toml.load(dir_path(base_dir + settings['paths']['fonts'] + blueprint['text']['preset'] + ".toml"))
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
                layer = template.clone()
                draw.composite(operator='atop', left=0, top=0, width=layer.width, height=layer.height, image=layer)
                draw(current)
                uts = str(int(time.time()))
                current.save(filename=buildpath + uts + "-template.png")

            # 4. Use wand to place text onto card (save intermediate files in _build)
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


def vartest(content, filename) -> None:
    filename_raw = filename.partition('.toml')

    with open(filename_raw[0] + ".output.json", "w") as outfile:
        json.dump(content, outfile, indent=4)


if __name__ == "__main__":
    cl_main()
