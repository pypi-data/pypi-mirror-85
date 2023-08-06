# coding: utf-8
"""openepda.__init__.py

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors
"""
from .main import OpenEpdaDataDumper, OpenEpdaDataLoader


try:
    from importlib.metadata import version
except ImportError:
    # Backport for Python < 3.8
    from importlib_metadata import version

try:
    __version__ = version("openepda")
except Exception:
    # we seem to have a local copy not installed without setuptools
    # so the reported version will be unknown
    __version__ = "unknown"


__all__ = [
    'OpenEpdaDataDumper',
    'OpenEpdaDataLoader',
    '__version__',
]
