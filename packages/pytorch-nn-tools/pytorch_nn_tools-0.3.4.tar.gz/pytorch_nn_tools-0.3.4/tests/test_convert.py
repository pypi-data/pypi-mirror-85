from collections import OrderedDict

from pytorch_nn_tools.convert import map_dict


def test_convert_keeps_type():
    data = {'apple': 4, 'banana': 3}
    result = map_dict(data, lambda key: key, lambda value: value+1)
    assert type(result) == dict

    data = OrderedDict({'apple': 4, 'banana': 3})
    result = map_dict(data, lambda key: key, lambda value: value+1)
    assert type(result) == OrderedDict
    assert result == OrderedDict({'apple': 5, 'banana': 4})
