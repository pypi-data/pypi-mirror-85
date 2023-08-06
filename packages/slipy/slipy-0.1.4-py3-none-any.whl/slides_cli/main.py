import slipy.version


def add_options(parser):
    parser.add_argument("-v", "--version", action="store_true", help=help["version"])


help = {"subparsers": """subcommand help""", "version": """show version"""}


def run(parser, args, e):
    if args.version:
        print(slipy.version.full_version)
    elif len(e.args) > 0 and e.args[0] == "'Namespace' object has no attribute 'func'":
        print(parser.format_help())
    else:
        raise
