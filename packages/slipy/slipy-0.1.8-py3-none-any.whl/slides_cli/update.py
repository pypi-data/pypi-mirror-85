import pathlib

import slipy.update


def add_parser(subparsers):
    update_p = subparsers.add_parser("update", help=help["."])
    update_p.set_defaults(func=update)


def update(args):
    slipy.update.update(pathlib.Path(".").absolute())


help = {".": """Update assets according to 'presentation.toml'"""}
