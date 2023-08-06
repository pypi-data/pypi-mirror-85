import pathlib

import slipy.view


def add_parser(subparsers):
    view_p = subparsers.add_parser("view", help=help["."])
    view_p.set_defaults(func=view)


def view(args):
    slipy.view.view(pathlib.Path(".").absolute())


help = {".": """Show a packaged presentation"""}
