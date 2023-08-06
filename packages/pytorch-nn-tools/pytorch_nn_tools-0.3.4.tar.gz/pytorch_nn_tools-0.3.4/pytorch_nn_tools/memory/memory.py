import torch
from torch import nn
from typing import Tuple


def dummy_batch(m: nn.Module, size: Tuple) -> torch.Tensor:
    return next(m.parameters()).new_empty(size=size).requires_grad_(False).uniform_(-1., 1.)
