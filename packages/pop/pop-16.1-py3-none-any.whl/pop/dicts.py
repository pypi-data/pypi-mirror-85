"""
Tools to work with dicts
"""
import warnings

import dict_tools.data
import dict_tools.update

__virtualname__ = "dicts"


def update(*args, **kwargs):
    warnings.warn(
        "Use `dict_tools.update.update()` instead", DeprecationWarning, stacklevel=1
    )
    return dict_tools.update.update(*args, **kwargs)


def traverse(*args, **kwargs):
    warnings.warn(
        "Use `dict_tools.data.traverse_dict_and_list()` instead", DeprecationWarning
    )
    return dict_tools.data.traverse_dict_and_list(*args, **kwargs)
