import pathlib
import inspect

import slipy.build


def add_parser(subparsers):
    build_p = subparsers.add_parser(
        "build", help=help["."], description=help["description"]
    )
    build_p.add_argument(
        "-d", "--update-dist", action="store_true", help=help["update_dist"]
    )
    build_p.add_argument(
        "-a", "--update-assets", action="store_true", help=help["update_assets"]
    )
    build_p.set_defaults(func=build)


help = {
    ".": """Build the presentation""",
    "description": """Build the presentation from user source, according to the selected template
        and theme, and collect all assets and distribution files (the files needed
        to visualize the presentation coming from the selected framework).
        """,
    "update_dist": """Update framework distribution in build folder""",
    "update_assets": """Update all assets in build folder""",
}


def build(args):
    slipy.build.build(
        pathlib.Path(".").absolute(),
        update_dist=args.update_dist,
        update_assets=args.update_assets,
    )
