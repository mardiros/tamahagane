"""
Forge your application registries.
"""

from importlib import metadata

from .scanner import Scanner, attach

__version__ = metadata.version("tamahagane")
__all__ = ["Scanner", "attach"]
