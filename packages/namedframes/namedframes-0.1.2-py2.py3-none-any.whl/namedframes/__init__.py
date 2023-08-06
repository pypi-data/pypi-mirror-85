"""Top-level package for namedframes."""

__author__ = """Ben Dilday"""
__email__ = "ben.dilday.phd@gmail.com"
__version__ = "0.1.2"

from .pandas_frames import PandasNamedFrame

try:
    from .spark_frames import SparkNamedFrame

    __all__ = ["PandasNamedFrame", "SparkNamedFrame"]
    _has_pyspark = True
except ModuleNotFoundError:
    __all__ = ["PandasNamedFrame"]
    _has_pyspark = False
