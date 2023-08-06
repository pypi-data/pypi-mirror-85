import pathlib
import importlib

import toml


def load_cfg(project_dir="."):
    project_dir = pathlib.Path(project_dir).absolute()
    return toml.load(project_dir / "presentation.toml")


def dump_cfg(presentation_cfg, project_dir="."):
    project_dir = pathlib.Path(project_dir).absolute()

    with open(project_dir / "presentation.toml", "w") as fd:
        toml.dump(presentation_cfg, fd)


def get_norm_title(project_dir="."):
    """
    Normalize title to be used as file name.
    """
    presentation_cfg = load_cfg(project_dir)
    return presentation_cfg["title"].lower().replace(" ", "_")


def check_slipy_project(project_dir="."):
    project_dir = pathlib.Path(project_dir).absolute()
    if not (project_dir / "presentation.toml").exists():
        raise RuntimeError(f"'{project_dir}' is not a slipy project")


def switch_framework(framework):
    try:
        return importlib.import_module(f"..{framework}", package=__package__)
    except ModuleNotFoundError:
        raise ValueError(f"unknown framework selected: {framework}")
