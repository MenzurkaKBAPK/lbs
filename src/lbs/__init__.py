"""LBS educational programming language."""

from .errors import LbsError
from .interpreter import run_source

__version__ = "0.1.0"

__all__ = ["LbsError", "run_source"]
