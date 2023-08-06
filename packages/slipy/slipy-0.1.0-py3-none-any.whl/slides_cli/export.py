import pathlib

import slipy.export


def add_parser(subparsers):
    export_p = subparsers.add_parser("export", help=help["."])
    export_p.set_defaults(func=export)


def export(args):
    slipy.export.export(pathlib.Path(".").absolute())


help = {".": """Make the package to be exported"""}
