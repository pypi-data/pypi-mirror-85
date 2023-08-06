import pathlib

import toml

here = pathlib.Path(__file__).parent

reveal_cfg = toml.load(here / "reveal.toml")
