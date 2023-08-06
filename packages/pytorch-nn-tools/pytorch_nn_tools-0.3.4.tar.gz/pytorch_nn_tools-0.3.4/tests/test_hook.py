from typing import Any

import pytest
import torch
from pytorch_nn_tools.hook import Hooking, get_output_size
from torch import nn


class DummyLinear(nn.Module):
    """
    Dummy linear class with predefined weights for testing.
    """

    def __init__(self, weight, bias):
        super().__init__()
        assert weight.shape[0] == bias.shape[0]
        assert weight.ndim == 2
        assert bias.ndim == 1
        self.linear = nn.Linear(weight.shape[1], weight.shape[0])
        with torch.no_grad():
            self.linear.weight.copy_(weight)
            self.linear.bias.copy_(bias)

    def forward(self, *input: Any, **kwargs: Any):
        return self.linear(*input, **kwargs)


@pytest.fixture
def linear1():
    return DummyLinear(weight=torch.tensor([[1., 0.], [0., 1.]]), bias=torch.tensor([0.6, 0.8]))


@pytest.fixture
def linear2():
    return DummyLinear(weight=torch.tensor([[100, 1]]), bias=torch.tensor([0.09]))


@pytest.fixture
def x():
    return torch.tensor((5., 7.))


def test_dummy_linear(linear1, linear2, x):
    with torch.no_grad():
        r1 = linear1(x)
        r2 = linear2(r1)

    assert r1.allclose(torch.tensor((5.6, 7.8)))
    assert r2.allclose(torch.tensor(567.89))


def test_hooking_and_get_output_size(linear1, linear2, x):
    module = nn.Sequential(linear1, linear2)
    with Hooking([linear1, linear2], get_output_size) as h:
        module(x)

    assert h.results() == [[torch.Size([2])], [torch.Size([1])]]


def test_hooking_output_results(linear1, linear2, x):
    module = nn.Sequential(linear1, linear2)

    with Hooking([linear1], lambda module_, input, output: output.detach()) as h:
        module(x)
        module(x * 0)

    assert len(h.results()) == 1
    assert len(h.results()[0]) == 2
    for r, expected in zip(
        h.results()[0],
        [torch.tensor([5.6, 7.8]), torch.tensor([0.6, 0.8])]
    ):
        assert r.allclose(expected)

