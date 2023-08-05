# -*- coding: utf-8 -*-
"""

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors

Changelog
---------
2020.04.28
    Initial commit
"""

try:
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    safe_load = yaml.load
    dump_long = yaml.dump

    yaml2 = YAML(typ="safe")
    dump_short = yaml2.dump
except ImportError:
    from yaml import safe_load
    from yaml import dump
    from functools import partial

    dump_long = partial(dump, default_flow_style=False)
    dump_short = partial(dump, default_flow_style=True)


REQUIRED_NAZCA_VERSION = "0.5.12"

try:
    import nazca as nd

    if nd.__version__ != REQUIRED_NAZCA_VERSION:
        print(
            "This version of openepda requires nazca-{}. "
            "Version {} is installed.".format(
                REQUIRED_NAZCA_VERSION, nd.__version__
            )
        )
        HAS_NAZCA_DESIGN = False
    else:
        nd.clear_layout()
        # nd.clear_xsections()
        # nd.clear_layers()
        HAS_NAZCA_DESIGN = True
except ImportError:
    HAS_NAZCA_DESIGN = False


REQUIRED_KLAYOUT_VERSION = "0.26.4"

try:
    import klayout.dbcore as dbcore
    HAS_KLAYOUT = True
    Cell = dbcore.Cell
    Layout = dbcore.Layout
    LayerInfo = dbcore.LayerInfo
except ImportError:
    HAS_KLAYOUT = False
