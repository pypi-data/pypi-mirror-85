import pathlib
import importlib

import toml

# slipy project identification
# ----------------------------


def find_project_dir(folder):
    path = pathlib.Path(folder).absolute()

    for project_dir in [path] + list(path.parents):
        if (project_dir / "presentation.toml").exists():
            return project_dir

    raise ValueError(f"'{folder}' is not inside any 'slipy' project")


def check_slipy_project(project_dir="."):
    project_dir = pathlib.Path(project_dir).absolute()
    if not (project_dir / "presentation.toml").exists():
        raise RuntimeError(f"'{project_dir}' is not a slipy project")


# cfg management
# --------------


def load_cfg(project_dir):
    project_dir = pathlib.Path(project_dir)
    return toml.load(project_dir / "presentation.toml")


def dump_cfg(presentation_cfg, project_dir):
    project_dir = pathlib.Path(project_dir)

    with open(project_dir / "presentation.toml", "w") as fd:
        toml.dump(presentation_cfg, fd)


# other utilities
# ---------------


def get_norm_title(folder="."):
    """
    Normalize title to be used as file name.
    """
    project_dir = find_project_dir(folder)
    presentation_cfg = load_cfg(project_dir)
    return presentation_cfg["title"].lower().replace(" ", "_")


def switch_framework(framework):
    try:
        return importlib.import_module(f"..{framework}", package=__package__)
    except ModuleNotFoundError:
        raise ValueError(f"unknown framework selected: {framework}")
