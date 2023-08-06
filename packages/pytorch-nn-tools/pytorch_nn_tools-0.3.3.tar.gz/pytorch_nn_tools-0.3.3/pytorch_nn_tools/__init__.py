"""Top-level package for pytorch-nn-tools."""

__author__ = """SergeM"""
__email__ = 'serge-m@users.noreply.github.com'

from .version import __version__

from .hook import Hook, _hook_inner
from .structure import get_output_sizes, LayerSize, NameGetter
from .memory import dummy_batch


__all__ = ["Hook", "_hook_inner", "get_output_sizes", "LayerSize", "NameGetter", "dummy_batch", "__version__"]
