from collections import defaultdict
from pathlib import Path
from typing import Dict, Union, Any, Iterable
import enum

import torch
from pytorch_nn_tools.convert import map_dict
from torch.utils.tensorboard import SummaryWriter


@enum.unique
class Marker(enum.Enum):
    ITERATION = 'iteration'
    EPOCH = 'epoch'


MetricNameType = Union[str, Marker]
MetricType = Dict[MetricNameType, Any]


class MetricProcessor:
    def __call__(self, data: MetricType) -> MetricType:
        return data

    def __add__(self, other):
        processors = []
        for x in [self, other]:
            if isinstance(x, MetricPipeline):
                processors.extend(x._processors)
            elif isinstance(x, MetricProcessor):
                processors.append(x)
            else:
                raise ValueError(f"Cannot add MetricProcessor and {other} of type {type(other)}")
        return MetricPipeline(*processors)


class MetricPipeline(MetricProcessor):
    def __init__(self, *processors):
        self._processors = processors

    def __call__(self, data: MetricType) -> MetricType:
        for p in self._processors:
            data = p(data)
        return data


class MetricAggregator(MetricProcessor):
    DEFAULT_SKIPPED = tuple(Marker)

    def __init__(self, skip_names: Iterable[MetricNameType] = DEFAULT_SKIPPED):
        """
        Aggregates metrics values over time
        >>> agg = MetricAggregator(["b"])
        >>> input1 = {'a': 1, 'b': 10}
        >>> input2 = {'a': 5, 'b': 20}
        >>> ret = agg(input1)
        >>> assert ret == input1
        >>> ret = agg(input2)
        >>> assert ret == input2
        >>> assert agg.aggregate() == {'a': (1+5)/2}
        """
        self._metrics = defaultdict(list)
        self.skipped = set(skip_names)

    def __call__(self, data: MetricType) -> MetricType:
        for k, v in data.items():
            if k not in self.skipped:
                self._metrics[k].append(v)
        return data

    def aggregate(self) -> Dict:
        return {
            k: sum(vs) / (len(vs) if vs else 1.)
            for k, vs in self._metrics.items()
        }


def detach_and_get_if_tensor(x):
    return x.detach().item() if torch.is_tensor(x) else x


class MetricMod(MetricProcessor):
    DEFAULT_SKIPPED = tuple(Marker)

    def __init__(self, name_fn=lambda x: x, value_fn=detach_and_get_if_tensor,
                 skip_names: Iterable[MetricNameType] = DEFAULT_SKIPPED):
        self.name_fn = name_fn
        self.value_fn = value_fn
        self.skipped = set(skip_names)

    def __call__(self, data: MetricType) -> MetricType:
        return map_dict(data, key_fn=self.name_fn, value_fn=self.value_fn, skip_keys=self.skipped)


class MetricLogger(MetricProcessor):
    def __init__(self, path: Union[str, Path]):
        path = Path(path)
        path.mkdir(exist_ok=True, parents=True)
        self.writer = SummaryWriter(path)

    def __call__(self, data: MetricType) -> MetricType:
        iteration = data.pop(Marker.ITERATION, None)
        if iteration is None:
            iteration = data.pop(Marker.EPOCH, None)
        if iteration is not None:
            for name, value in data.items():
                self.writer.add_scalar(name, value, iteration)

        return data

    def close(self):
        self.writer.close()


mod_name_train = MetricMod(
    name_fn=lambda name: f"train.{name}",
)
mod_name_val = MetricMod(
    name_fn=lambda name: f"val.{name}",
)
