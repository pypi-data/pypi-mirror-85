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
    folder = pathlib.Path(folder)
    collect_dir = folder / title
    build_dir = folder / "build"
    if not build_dir.exists():
        build_dir.mkdir()

    logger.debug("Create 'src.tmp'")
    collect_dir.mkdir(exist_ok=True)
    src_dir = folder / "src.tmp"
    src_dir.mkdir()

    dev_files = utils.switch_framework(framework).dev_files

    gen_assets = [p.name for p in [src_dir, collect_dir, build_dir]]
    gen_assets.extend(dev_files)
    for f in folder.iterdir():
        if f.name not in gen_assets:
            if f.is_dir():
                shutil.copytree(str(f.absolute()), src_dir)
            else:
                shutil.copy2(str(f.absolute()), src_dir)

    shutil.move(str(src_dir.rename("src")), collect_dir)
    for fd in dev_files:
        shutil.copytree(str(folder / fd), collect_dir / fd)

    archive = compress(collect_dir)
    shutil.rmtree(collect_dir)

    archive = pathlib.Path(archive)
    if (build_dir / archive.name).exists():
        (build_dir / archive.name).unlink()

    shutil.move(str(archive), build_dir)
