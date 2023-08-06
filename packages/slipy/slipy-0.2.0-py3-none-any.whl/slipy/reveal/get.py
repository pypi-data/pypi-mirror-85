"""
Get reveal version.

.. todo::
    manage a cache:

        - the reveal project should be downloaded and built in
          '~/.local/share/slipy` (allow for a prefix to be passed instead and
           register it in a file relative to this one)
        - allow for a CLI option to explicitly invalidate the cache,
          automatically invalidate after a couple of months

"""
import pathlib
import shutil
import subprocess
import sys
import logging

import requests
import pygit2

from slipy_assets.reveal import reveal_cfg

from ..utils import archive

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(levelname)s]: %(message)s (%(name)s)",
)
logger = logging.getLogger(__name__)


def build_dist(folder):
    logger.info(f"Build dist: reveal at '{folder}'")
    try:
        logger.info(f"Install: try to build '{folder}' with yarn")
        subprocess.run(["yarn"], cwd=folder)
        subprocess.run(["yarn", "build"], cwd=folder)
    except FileNotFoundError:
        logger.info(f"Install: yarn not found, try to build '{folder}' with npm")
        subprocess.run(["npm", "install"], cwd=folder)
        subprocess.run(["npm", "run-script", "build"], cwd=folder)


def extract_essentials(folder, dest):
    logger.info(f"Export dist: from '{folder}' to '{dest}'")

    shutil.copytree(folder / "dist", dest / "dist")
    logger.debug("Export dist: copied 'dist'")

    shutil.copytree(folder / "plugin", dest / "plugin")
    logger.debug("Export dist: copied 'plugin'")


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def get_reveal_release(project_dir, tmp_folder):
    project_dir = pathlib.Path(project_dir).absolute()
    zip_dir = project_dir / "dist.zip"

    api_url = "https://api.github.com/repos/hakimel/reveal.js/releases/latest"
    infos = requests.get(api_url).json()

    download_url(infos["zipball_url"], zip_dir)

    archive.uncompress(zip_dir, project_dir)

    for el in project_dir.iterdir():
        if el.is_dir():
            release_dir = el.absolute()

    shutil.move(release_dir, tmp_folder)
    zip_dir.unlink()


def get_reveal_git(project_dir, tmp_folder):
    logger.info(f"Clone repo: from '{url}' into '{tmp_folder}'")
    pygit2.clone_repository(url, tmp_folder)


def get_reveal(project_dir, force_rebuild):
    project_dir = pathlib.Path(project_dir).absolute()

    url = reveal_cfg["repo"]["url"]
    tmp_folder = project_dir / "reveal_tmp"
    dest = project_dir / ".reveal_dist"

    shutil.rmtree(tmp_folder, ignore_errors=True)

    if dest.exists():
        auth = input(
            f"'{dest}' already existing, do you want to continue removing it? [Y/n]"
        )
        if auth.lower() not in ["y", "yes"]:
            print("Nothing done.")
            return
        else:
            logger.info(f"Removed: old reveal.js in '{tmp_folder}' removed")
            shutil.rmtree(dest)

    # get_reveal_git(project_dir, tmp_folder)
    get_reveal_release(project_dir, tmp_folder)

    if force_rebuild:
        build_dist(tmp_folder)
    extract_essentials(tmp_folder, dest)

    shutil.rmtree(tmp_folder)
