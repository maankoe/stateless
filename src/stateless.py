from copy import deepcopy as copy
from typing import Iterable, Any, Mapping, TypeVar, Callable, Optional, Union

T = TypeVar("T")


def stateless(
    decorated,
    copy_func: Optional[Callable[[T], T]] = copy,
    arg_copy_funcs: Optional[
        Union[Mapping[str, Callable[[T], T]], Iterable[Callable[[T], T]]]
    ] = None,
):
    def _stateless(*args, **kwargs):
        return decorated(
            *_copy_args(args, copy_func, arg_copy_funcs),
            **_copy_kwargs(kwargs, copy_func, arg_copy_funcs)
        )

    return _stateless


def _copy_args(
    args: Iterable[T],
    copy_func: Callable[[T], T],
    arg_copy_funcs: Optional[Iterable[Callable[[T], T]]] = None,
) -> Iterable[Any]:
    if arg_copy_funcs is None:
        return (copy_func(arg) for arg in args)
    else:
        return (arg_copy_func(arg) for arg_copy_func, arg in zip(arg_copy_funcs, args))


def _copy_kwargs(
    kwargs: Mapping[str, T],
    copy_func: Callable[[T], T],
    arg_copy_funcs: Optional[Mapping[str, Callable[[T], T]]] = None,
) -> Mapping[str, T]:
    if arg_copy_funcs is None:
        return {kw: copy_func(arg) for kw, arg in kwargs.items()}
    else:
        return {
            kw: arg_copy_funcs[kw](arg) if kw in arg_copy_funcs else copy_func(arg)
            for kw, arg in kwargs.items()
        }
