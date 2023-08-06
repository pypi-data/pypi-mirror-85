"""
https://github.com/fastai/

For the licence see licence/fastai_licence.txt
"""

from typing import Any
from torch import nn


def _hook_inner(m, i, o):
    return o


def is_listy(x: Any) -> bool:
    return isinstance(x, (tuple, list))


class Hook():
    "Create a hook on `m` with `hook_func`."

    def __init__(self, m: nn.Module, hook_func, detach: bool = True):
        self.hook_func, self.detach, self.stored = hook_func, detach, None
        self.hook = m.register_forward_hook(self.hook_fn)
        self.removed = False

    def hook_fn(self, module: nn.Module, input, output):
        "Applies `hook_func` to `module`, `input`, `output`."
        if self.detach:
            input = (o.detach() for o in input) if is_listy(input) else input.detach()
            output = (o.detach() for o in output) if is_listy(output) else output.detach()
        self.stored = self.hook_func(module, input, output)

    def remove(self):
        if not self.removed:
            self.hook.remove()
            self.removed = True

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.remove()
