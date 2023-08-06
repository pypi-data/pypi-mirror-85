import types
from typing import Callable, TypeVar

from weary.context import _decorate_with_context
from weary.method_registrations import method_registrations

T = TypeVar("T")


def property(clazz, function_name) -> Callable[..., Callable[..., T]]:
    if not hasattr(clazz, "_weary_base"):
        raise Exception(
            "You can only override properties for classes decorated "
            "with `@weary.model`."
        )

    def wrapper_builder(f: Callable[..., T]) -> Callable[..., T]:
        context_aware_function = _decorate_with_context(f)
        method_registrations[clazz._weary_base][function_name] = f
        setattr(
            clazz._weary_base,
            function_name,
            types.DynamicClassAttribute(context_aware_function, clazz._weary_base),
        )

        return f

    return wrapper_builder
