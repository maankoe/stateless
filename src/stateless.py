from copy import deepcopy as copy
from typing import Iterable, Any, Mapping


def stateless(decorated):
    def _stateless(*args, **kwargs):
        return decorated(*_copy_args(args), **_copy_kwargs(kwargs))
    return _stateless


def _copy_args(args: Iterable[Any]) -> Iterable[Any]:
    return (copy(arg) for arg in args)


def _copy_kwargs(kwargs: Mapping[str, Any]) -> Mapping[str, Any]:
    return {kw: copy(arg) for kw, arg in kwargs.items()}
