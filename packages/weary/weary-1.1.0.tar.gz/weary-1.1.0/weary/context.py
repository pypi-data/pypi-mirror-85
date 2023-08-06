import functools
from typing import TypeVar, Callable

T = TypeVar("T")


class WearyContext:
    def __init__(self) -> None:
        super(WearyContext, self).__init__()


def _decorate_with_context(method_impl: Callable) -> Callable:
    called = False
    result = None

    @functools.wraps(method_impl)
    def decorated_function(self):
        nonlocal called
        nonlocal result

        if called:
            return result

        ctx = WearyContext()

        result = method_impl(self, ctx)
        called = True

        return result

    return decorated_function
