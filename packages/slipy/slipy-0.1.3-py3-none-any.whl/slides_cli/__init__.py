import argparse

from . import new
from . import init
from . import update
from . import preview
from . import build
from . import view
from . import export
from . import inflate
from . import tutorial


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="subcommand help")

# new
new.add_parser(subparsers)

# init
init.add_parser(subparsers)

# update
update.add_parser(subparsers)

# preview
preview.add_parser(subparsers)

# build
build.add_parser(subparsers)

# view
view.add_parser(subparsers)

# export
export.add_parser(subparsers)

# inflate
inflate.add_parser(subparsers)

# tutorial
tutorial.add_parser(subparsers)


def run_slipy():
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError as e:
        if (
            len(e.args) > 0
            and e.args[0] == "'Namespace' object has no attribute 'func'"
        ):
            print(parser.format_help())
        else:
            raise
