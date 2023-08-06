"""
Show the presentation
"""
import pathlib

from . import utils


def view(folder):
    project_dir = utils.find_project_dir(folder)
    framework = utils.load_cfg(project_dir)["framework"]

    utils.switch_framework(framework).view.view(project_dir)
