import pathlib
import re

import frontmatter

from slipy_assets import Template, Slide


def update_build_context(data, src_dir="src"):
    src_dir = pathlib.Path(src_dir)
    slides_pattern = re.compile("\d*\.(html|md)")
    oth_patterns = {
        "head": re.compile("head.*\.(html|md)"),
        "foot": re.compile("foot.*\.(html|md)"),
    }

    head_path = None
    slides_paths = []
    oth_paths = {}
    for path in src_dir.iterdir():
        if slides_pattern.fullmatch(path.name):
            slides_paths.append(path)
        else:
            for name, pattern in oth_patterns.items():
                if pattern.fullmatch(path.name):
                    if name not in oth_paths:
                        oth_paths[name] = path
                        break
                    else:
                        raise RuntimeError("Only a single header file is allowed")

    slides = []
    for slide_path in sorted(slides_paths):
        with open(slide_path) as f:
            metadata, content = frontmatter.parse(f.read())

        try:
            force_html = metadata["force_html"]
            del metadata["force_html"]

            if force_html:
                force_format = "html"
        except KeyError:
            force_format = ""

        slide = Slide(metadata, content, force_format=force_format)
        slides.append(slide)

    data["slides"] = slides
    for name in oth_patterns:
        if name in oth_paths:
            with open(oth_paths[name]) as f:
                data[name] = f.read()
        else:
            data[name] = ""
