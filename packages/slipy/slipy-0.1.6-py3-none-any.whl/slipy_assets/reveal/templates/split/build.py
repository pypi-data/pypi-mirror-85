import pathlib
import re

import frontmatter

from slipy_assets import Template, Slide


def update_build_context(data, src_dir="src"):
    src_dir = pathlib.Path(src_dir)
    header_pattern = re.compile("head.*\.(html|md)")
    slides_pattern = re.compile("\d*\.(html|md)")

    head_path = None
    slides_paths = []
    for path in src_dir.iterdir():
        if slides_pattern.fullmatch(path.name):
            slides_paths.append(path)
        elif header_pattern.fullmatch(path.name):
            if head_path is None:
                head_path = path
            else:
                raise RuntimeError("Only a single header file is allowed")

    slides = []
    for slide_path in sorted(slides_paths):
        with open(slide_path) as f:
            metadata, content = frontmatter.parse(f.read())

        slide = Slide(metadata, content)
        slides.append(slide)

    data["slides"] = slides
    data["head"] = ""
    if head_path is not None:
        with open(head_path) as f:
            data["head"] = f.read()
