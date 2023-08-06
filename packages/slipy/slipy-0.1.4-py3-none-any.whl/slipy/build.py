"""
Build everything needed to *show* the presentation, if possible in a single file
"""
import pathlib
import shutil

from jinja2 import Environment, FileSystemLoader

from slipy_assets import Template

from . import utils
from .reveal import reload


def build(folder, update_dist=False, update_assets=False):
    project_dir = utils.find_project_dir(folder)
    build_dir = project_dir / "build"
    src_dir = project_dir / "src"

    presentation_cfg = utils.load_cfg(project_dir)
    template_name = presentation_cfg["template"]["name"]
    framework = presentation_cfg["framework"]
    template = Template(template_name, framework)

    # prepare environment
    # -------------------
    if not (build_dir).exists():
        build_dir.mkdir()

    env = Environment(loader=FileSystemLoader(str(project_dir.absolute())))

    # load data
    # ---------
    data = {}

    data["reveal_dist"] = ".reveal_dist"
    data["theme"] = presentation_cfg["theme"]["name"]

    template.update_build_context(data, src_dir)

    # dump the result
    # ---------------
    j_template = env.get_template(".presentation/template.html")
    stream = j_template.stream(data)
    stream.dump(str(build_dir / "index.html"))

    # add the liver reloading script
    with open(build_dir / "index.html") as fd:
        index_html = fd.read()

    index_html = index_html.replace("</body>", reload.WEBSOCKET_JS_TEMPLATE)

    with open(build_dir / "index.html", "w") as fd:
        fd.write(index_html)

    if not (build_dir / pathlib.Path(reload.httpwatcher_script_url).name).exists():
        shutil.copy2(str(reload.httpwatcher_script_url), str(build_dir))

    # provide assets
    # --------------
    assets_dir = src_dir / "assets"
    if not (build_dir / "assets").exists() or update_assets:
        shutil.rmtree(build_dir / "assets", ignore_errors=True)
        shutil.copytree(str(assets_dir), str(build_dir / "assets"))

    # provide dist
    # ------------
    dist = project_dir / utils.switch_framework(framework).dist_files
    if not (build_dir / dist.name).exists() or update_dist:
        shutil.rmtree(build_dir / dist.name, ignore_errors=True)
        shutil.copytree(str(dist), str(build_dir / dist.name))
