from typing import Callable, Iterable, Dict


def map_dict(dictionary,
             key_fn: Callable = lambda key: key,
             value_fn: Callable = lambda value: value,
             skip_keys: Iterable = ()) -> Dict:
    """
    Converts all the keys and values of a dictionary according to the
    specified mapping functions, except for the (key, value) pairs where
    `key` belongs to `skip_keys`.

    >>> data = {'a': 1, 'b': 2, 'c':3}
    >>> expected = {'A': 11, 'b': 2, 'C': 13}
    >>> assert map_dict(data, lambda key: key.upper(), lambda value: value + 10, skip_keys='b') == expected

    """
    skip_keys = set(skip_keys)
    return dict([
        (
            (key_fn(key), value_fn(value))
            if key not in skip_keys
            else (key, value)
        )
        for key, value in dictionary.items()
    ])
