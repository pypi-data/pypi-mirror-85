import pathlib

import slipy.inflate


def add_parser(subparsers):
    inflate_p = subparsers.add_parser("inflate", help=help["."])
    inflate_p.set_defaults(func=inflate)


def inflate(args):
    slipy.inflate.inflate(pathlib.Path(".").absolute())


help = {".": """Restore develop environment from a package"""}
