#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import toml
import wand


def cl_main() -> None:
    """
    Entrypoint of command line interface.
    """

    arg_parser = argparse.ArgumentParser(description='Cardmage open-source card builder')
    arg_parser.add_argument("path", nargs="+", help="Path to the card's root TOML file", type=dir_path)
    arg_parser.add_argument("-p", "--print", help="Render card in print quality", default=False, action="store_true")

    args = arg_parser.parse_args()
    # args.print enthält die Info, ob der print-Switch gesetzt ist oder nicht

    blueprint = dict()
    working_dir = os.getcwd()

    for card in args.path:
        blueprint = toml.load(card)
        buildpath = os.path.join(working_dir, '_build')
        distpath = os.path.join(working_dir, 'dist')

        if not os.path.exists(buildpath):
            os.mkdir(buildpath)

        if not os.path.exists(distpath):
            os.mkdir(distpath)

        print(blueprint)
        vartest(blueprint, card)

        # 2. Load the necessary preset .toml files based on blueprint data (fonts, layouts)
        # 3. Use wand to construct the final card (save intermediate files in _build)
        # 4. Use wand to place text onto card (save intermediate files in _build)
        # 5. Save image in dist
        # 6. Remove _build and it's contents
        shutil.rmtree(buildpath)


def dir_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)


def vartest(content, filename):
    filename_raw = filename.partition('.toml')

    with open(filename_raw[0] + ".output.json", "w") as outfile:
        json.dump(content, outfile, indent=4)


if __name__ == "__main__":
    cl_main()
