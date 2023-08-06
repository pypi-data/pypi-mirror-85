import slipy.new


def add_parser(subparsers):
    new_p = subparsers.add_parser("new", help=help["."])
    new_p.add_argument("name", nargs=1)
    new_p.add_argument("-f", "--framework", default="reveal")
    new_p.add_argument("--pdf", help=help["pdf"])
    new_p.set_defaults(func=new)


def new(args):
    slipy.new.new(args.name[0], args.framework)


help = {".": """Create a new project""", "pdf": """create a beamer presentation"""}
