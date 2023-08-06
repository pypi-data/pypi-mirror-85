"""
Show a live updating version of the presentation.

.. todo::
    try to use a minimal build: do not create fully built object, if posssible,
    in order to save on update time

"""

import pathlib

from . import utils


def preview(folder):
    project_dir = utils.find_project_dir(folder)

    framework = utils.load_cfg(project_dir)["framework"]

    utils.switch_framework(framework).view.preview(project_dir)
