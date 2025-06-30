
import inspect
from inspect import Parameter, Signature
import functools
from typing import Callable, Any


def ignore_unexpected_args_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    '''
    未定義のパラメータを無視する function wrapper (decorator)
    '''

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return ignore_unexpected_args_wrapper(func, *args, **kwargs)

    return wrapper



def ignore_unexpected_args_wrapper(func:Callable[..., Any], *args, **kwargs) -> Any:
    '''
    未定義のパラメータを無視する function wrapper
    '''

    def filter_args(args: list) -> dict:
        sig:Signature = inspect.signature(func)

        # If *args exists, it is unlimited so return all of it.
        if any(map(lambda p: p.kind == Parameter.VAR_POSITIONAL, sig.parameters.values())):
            return args

        args_max_len = len([p for p in sig.parameters.values() if p.kind == Parameter.POSITIONAL_OR_KEYWORD])
        res_args = args[0:args_max_len]
        return res_args

    def filter_kwargs(kwargs: dict) -> dict:
        sig:Signature = inspect.signature(func)

        # If **kwargs exists, it is unlimited so return all of it.
        if any(map(lambda p: p.kind == Parameter.VAR_KEYWORD, sig.parameters.values())):
            return kwargs

        _params = list(filter(lambda p: p.kind in {Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD},
                              sig.parameters.values()))

        res_kwargs = {
            param.name: kwargs[param.name]
            for param in _params if param.name in kwargs
        }
        return res_kwargs

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        args   = filter_args(args)
        kwargs = filter_kwargs(kwargs)
        return func(*args, **kwargs)

    return wrapper(*args, **kwargs)

