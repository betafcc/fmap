from typing import Callable, TypeVar
from functools import reduce


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def const(a: A) -> Callable[[B], A]:
    return lambda b: a


def compose(f: Callable[[B], C],
            g: Callable[[A], B],
            ) -> Callable[[A], C]:
    """
    Compose function in the only way I found
    to keep mypy happy and at the same time be
    reasonable optimized and keep a nice __name__
    """

    args      = [f, g]
    functions = []  # type: ignore
    name      = []  # type: ignore

    for func in args:
        try:
            name.append(func.__name__)
        except AttributeError:
            name.append(repr(func))

        try:
            functions += getattr(func, '__functions')
        except AttributeError:
            functions.append(func)

    def _compose(arg: A) -> C:
        result : C
        result = reduce(lambda acc, n: n(acc),  # type: ignore
                        reversed(functions),
                        arg)
        return result

    _compose.__name__    = ' . '.join(name)
    setattr(_compose, '__functions', functions)

    return _compose
