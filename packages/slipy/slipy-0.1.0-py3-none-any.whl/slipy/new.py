import pathlib

import toml

from slipy_assets import template_cfg, Template, Theme

from . import utils
from . import update


def new(name, framework):
    project_dir = pathlib.Path(name)
    project_dir.mkdir()

    utils.switch_framework(framework).init(project_dir)

    presentation_cfg = template_cfg.copy()
    presentation_cfg["title"] = name
    presentation_cfg[framework] = utils.switch_framework(framework).set_initial_cfg(
        name
    )

    utils.dump_cfg(presentation_cfg, project_dir)


def checkout_assets(folder):
    project_dir = pathlib.Path(folder)

    presentation_cfg = utils.load_cfg(project_dir)
    framework = presentation_cfg["framework"]

    assets_dir = project_dir / ".presentation"
    assets_dir.mkdir(exist_ok=True)

    update.update(project_dir)
