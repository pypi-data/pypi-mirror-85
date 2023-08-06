import inspect

from .. import utils
from . import assets
from . import get
from . import view


def set_initial_cfg(name):
    reveal_cfg = {}
    reveal_cfg["dist_dir"] = ".reveal_dist"
    reveal_cfg["plugins"] = ["math"]

    return reveal_cfg


def dump_gitignore(project_dir):
    gitignore = inspect.cleandoc(
        """
        build
        .reveal_dist
        .presentation
        """
    )
    with open(project_dir / ".gitignore", "w") as fd:
        fd.write(gitignore)


def init(project_dir, force_rebuild=False):
    get.get_reveal(project_dir, force_rebuild)


dist_files = ".reveal_dist"
dev_files = [".presentation"]


def clean(folder):
    """
    Clean unneeded generated files
    """
    pass
