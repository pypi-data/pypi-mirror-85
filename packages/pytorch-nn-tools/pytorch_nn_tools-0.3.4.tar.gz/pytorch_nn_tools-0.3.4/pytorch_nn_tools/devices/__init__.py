import collections

import torch


def apply_recursively(func, x):
    """
    Apply `func` recursively to `x`.

    >>> result = apply_recursively(\
            lambda val: val+1, {'a': 10, 'b': [20,30,{'c':40}]})
    >>> assert result == {'a': 11, 'b': [21,31,{'c':41}]}
    >>> from collections import OrderedDict
    >>> result = apply_recursively(\
            lambda val: val+1,\
            OrderedDict([ \
                ('a', 10),  \
                ('b', (20,30)) \
            ]) \
        )
    >>> assert result == OrderedDict([('a', 11), ('b', (21,31))])
    >>> assert type(result) == OrderedDict
    >>> assert type(result['b']) == tuple
    """
    if isinstance(x, collections.abc.Sequence):
        return type(x)([apply_recursively(func, i) for i in x])
    if isinstance(x, collections.abc.Mapping):
        return type(x)(
            (k, apply_recursively(func, v))
            for k, v in x.items()
        )
    return func(x)


def to_device(data, device):
    """
    Sends the input to a given device.

    If the input is a Tensor it uses non_blocking=True for speed up.
    Some explanation can be found here https://discuss.pytorch.org/t/should-we-set-non-blocking-to-true/38234/7
    """

    def _inner(x):
        if isinstance(x, torch.Tensor):
            return x.to(device, non_blocking=True)
        elif hasattr(x, "to_device"):
            return x.to_device(device)
        else:
            return x

    return apply_recursively(_inner, data)
