#!/usr/bin/env python3

import argparse
import os
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

        if not os.path.exists(buildpath):
            os.mkdir(buildpath)

        # 2. Load the necessary preset .toml files based on blueprint data (fonts, layouts)
        # 3. Use wand to construct the final card
        # 4. Use wand to place text onto card
        # 5. Save image in _build


def dir_path(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)


if __name__ == "__main__":
    cl_main()
