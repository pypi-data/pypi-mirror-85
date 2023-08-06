import pathlib

import slipy.preview


def add_parser(subparsers):
    preview_p = subparsers.add_parser("preview", help=help["."])
    preview_p.set_defaults(func=preview)


def preview(args):
    slipy.preview.preview(pathlib.Path(".").absolute())


help = {".": """Run a live updating version of the presentation"""}
