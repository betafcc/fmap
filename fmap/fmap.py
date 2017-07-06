from typing import Sequence, TypeVar, Callable, Generic, Union, overload
from functools import reduce


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
T = TypeVar('T')


class fmap(Generic[A, B], Sequence[B]):
    @overload
    def __init__(self,
                 pipe   : Callable[[A], B],
                 source : Sequence[A],
                 ) -> None:
        ...

    @overload
    def __init__(self,
                 pipe   : Callable[[A], B],
                 source : 'fmap[T, A]',
                 ) -> None:
        ...

    def __init__(self, pipe, source) -> None:  # type: ignore
        if isinstance(source, fmap):
            self.__pipe   = compose(pipe, source.__pipe)  # type: ignore
            self.__source = source.__source  # type: ignore
        else:
            self.__pipe   = pipe
            self.__source = source

    def __len__(self) -> int:
        return len(self.__source)

    def __repr__(self) -> str:
        try:
            _pipe = self.__pipe.__name__
        except:
            _pipe = repr(self.__pipe)
        return f'{self.__class__.__name__}({_pipe}, {repr(self.__source)})'

    @overload
    def __getitem__(self, index: int) -> B:
        ...

    @overload
    def __getitem__(self, slice: slice) -> 'fmap[A, B]':
        ...

    def __getitem__(self,  # type: ignore
                    query: Union[int, slice]
                    ) -> Union[B, 'fmap[A, B]']:
        if isinstance(query, int):
            return self.__pipe(self.__source[query])
        elif isinstance(query, slice):
            return fmap(self.__pipe, self.__source[query])
        else:
            raise TypeError(
                'fmap only supports int and slice for indexing'
            )


def compose(f: Callable[[B], C],
            g: Callable[[A], B],
            ) -> Callable[[A], C]:
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
