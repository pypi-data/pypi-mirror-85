from .. import utils
from . import assets
from . import get
from . import view


def set_initial_cfg(name):
    reveal_cfg = {}
    reveal_cfg["dist_dir"] = ".reveal_dist"
    reveal_cfg["plugins"] = ["math"]

    return reveal_cfg


def init(project_dir):
    get.get_reveal(project_dir)


dist_files = ".reveal_dist"
dev_files = [".presentation"]


def clean(folder):
    """
    Clean unneeded generated files
    """
    pass
