import sys
import pathlib
import importlib
import shutil
import distutils.dir_util

import toml

# import framewokrs
from . import beamer
from . import reveal

here = pathlib.Path(__file__).parent

template_cfg = toml.load(here / "presentation.toml")


class Template:
    def __init__(self, name, framework):
        path = here / framework / "templates" / name

        self.template = path / "template.html"
        self.options = toml.load(path / "options.toml")
        self.examples = path / "examples"

        try:
            sys.path.insert(0, str(path.absolute()))
            self.update_build_context = importlib.import_module(
                "build"
            ).update_build_context
        except ModuleNotFoundError:
            self.update_build_context = lambda *args, **kwargs: None
        finally:
            sys.path.pop(0)

    def unpack(self, assets_dir):
        shutil.copy2(self.template, assets_dir)
        src_dir = assets_dir.parent.absolute() / "src"
        # unpack examples only if src does not exist or is empty
        if not src_dir.exists() or len(list(src_dir.iterdir())) == 0:
            # since I don't want to copy the folder but only the content
            # I have to use distutils.dir_util instead of shutil.copytree
            distutils.dir_util.copy_tree(str(self.examples), str(src_dir))


class Slide:
    def __init__(self, metadata, content, force_format=""):
        self.metadata = metadata
        self.content = content
        self.force_format = force_format


class Theme:
    def __init__(self, name, framework):
        path = here / framework / "themes"
        self.style = path / (name + ".css")

    def unpack(self, assets_dir):
        shutil.copy2(self.style, assets_dir)
