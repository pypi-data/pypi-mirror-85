import pathlib
import re

from rich.console import Console
from rich.markdown import Markdown

tutorial_dir = pathlib.Path(__file__).parent
console = Console()


def display_tutorial(name):
    paths = [
        t for t in tutorial_dir.iterdir() if re.fullmatch(f"\d*\.{name}.md", t.name)
    ]
    if len(paths) == 1:
        path = paths[0]
    elif len(paths) == 0:
        raise FileNotFoundError(f"tutorial '{name}' not available")
    else:
        raise RuntimeError(f"Too many tutorials found matching '\d*\.{name}.md'")

    with open(path) as fd:
        tutorial_text = fd.read()

    with console.pager():
        console.print(Markdown(tutorial_text))


def available_tutorials():
    tutorials = []

    for path in tutorial_dir.iterdir():
        if path.suffix == ".md":
            tutorials.append(path.stem)

    tutorials = [".".join(t.split(".")[1:]) for t in sorted(tutorials)]

    return tutorials


def print_available_tutorials():
    tutorials = available_tutorials()

    tutext = ""
    for tut in tutorials:
        tutext += f"- {tut}\n"

    console.print("[yellow]Available tutorials[/]:")
    console.print(Markdown(tutext))
