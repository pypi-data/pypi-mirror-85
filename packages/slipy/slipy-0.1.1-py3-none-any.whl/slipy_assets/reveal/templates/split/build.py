import pathlib
import re

import frontmatter

from slipy_assets import Template, Slide


def update_build_context(data, src_dir="src"):
    slides_dir = pathlib.Path(src_dir)
    slides_pattern = re.compile("\d*\.(html|md)")

    slides_paths = []
    for path in slides_dir.iterdir():
        if slides_pattern.fullmatch(path.name):
            slides_paths.append(path)

    slides = []
    for slide_path in sorted(slides_paths):
        with open(slide_path) as f:
            metadata, content = frontmatter.parse(f.read())

        slide = Slide(metadata, content)
        slides.append(slide)

    data["slides"] = slides
