# read version from version.txt
from os import path

__all__ = ["__version__"]

__version__ = open(path.join(path.dirname(__file__), '_version.txt')).read().strip()
