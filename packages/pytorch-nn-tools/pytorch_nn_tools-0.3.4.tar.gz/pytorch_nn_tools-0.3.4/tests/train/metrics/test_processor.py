import torch
from pytest import approx
from pytorch_nn_tools.train.metrics.processor import MetricMod

val1 = 10
val2 = 20.1


def test_metric_mod__handles_tensors():
    mm = MetricMod()
    result = mm({
        'metric1': val1,
        'metric2': torch.tensor(val2, requires_grad=True)
    })
    assert result == {
        'metric1': val1,
        'metric2': approx(val2)
    }


def test_metric_mod__handles_names():
    mm = MetricMod(name_fn=lambda x: x + "_new")
    result = mm({
        'metric1': val1,
        'metric2': val2
    })
    assert result == {
        'metric1_new': val1,
        'metric2_new': approx(val2)
    }


def test_processors_aggregation():
    mm1 = MetricMod(name_fn=lambda x: x + "_first")
    mm2 = MetricMod(name_fn=lambda x: x + "_second", value_fn=lambda x: x + 1)
    mm = mm1 + mm2
    result = mm({
        'metric1': val1,
    })
    assert result == {
        'metric1_first_second': val1+1,
    }
