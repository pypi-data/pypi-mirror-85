import functools
from typing import TypeVar, Type, Callable

from weary.method_registrations import method_registrations

T = TypeVar("T")


def model(f: Type[T]) -> Callable[..., T]:
    method_registrations[f] = dict()

    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        return _create(f, *args, **kw)

    wrapper._weary_base = f  # type: ignore

    return wrapper


def _create(t: Type[T], *args, **kw) -> T:
    """
    Create the instance with the given type
    :param t:
    :return:
    """
    result = t(*args, **kw)  # type: ignore

    if t not in method_registrations:
        raise Exception(f"{t} was not registered with @weary.model")

    return result
