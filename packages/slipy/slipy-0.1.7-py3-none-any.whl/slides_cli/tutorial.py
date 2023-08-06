import pathlib
import inspect

from . import tutorials


def add_parser(subparsers):
    tutorial_p = subparsers.add_parser(
        "tutorial", help=help["."], description=help["description"]
    )
    mode = tutorial_p.add_mutually_exclusive_group(required=True)
    mode.add_argument("name", nargs="?", help=help["name"])
    mode.add_argument("-a", "--show-all", action="store_true", help=help["show-all"])
    tutorial_p.set_defaults(func=tutorial)


help = {
    ".": """Show tutorials about using 'slipy'""",
    "description": """Collection of tutorials on using 'slipy'""",
    "name": """name of the select tutorial""",
    "show-all": """show all the names of available tutorials""",
}


def tutorial(args):
    if args.show_all:
        tutorials.print_available_tutorials()
    else:
        tutorials.display_tutorial(args.name)
