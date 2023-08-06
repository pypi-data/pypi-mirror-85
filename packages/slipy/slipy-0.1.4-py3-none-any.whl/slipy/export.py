"""
Make the object to export, consisting of a folder with:

- the presentation build by `build`
- the zipped dev environment

    - this should be shipped in order to be able to edit the presentation at a
      later time

"""
import pathlib
import importlib
import shutil
import logging

from . import build
from . import utils
from .utils.archive import compress

logger = logging.getLogger(__file__)


def export(folder):
    build.build(folder)
    title = utils.get_norm_title()
    framework = utils.load_cfg(folder)["framework"]

    utils.switch_framework(framework).clean(folder)
    collect(folder, title, framework)


def collect(folder, title, framework):
    project_dir = utils.find_project_dir(folder)
    collect_dir = project_dir / title
    build_dir = project_dir / "build"
    if not build_dir.exists():
        build_dir.mkdir()

    logger.debug("Create 'src.tmp'")
    tmp_dir = project_dir / "src.tmp"
    tmp_dir.mkdir()

    dev_files = utils.switch_framework(framework).dev_files

    generated_files = [p.name for p in [tmp_dir, build_dir]]
    for f in project_dir.iterdir():
        if f.name not in generated_files:
            if f.is_dir():
                shutil.copytree(str(f.absolute()), tmp_dir / f.name)
            else:
                shutil.copy2(str(f.absolute()), tmp_dir)

    tmp_dir.rename(collect_dir)

    archive = compress(collect_dir)
    shutil.rmtree(collect_dir)

    archive = pathlib.Path(archive)
    if (build_dir / archive.name).exists():
        (build_dir / archive.name).unlink()

    shutil.move(str(archive), build_dir)
