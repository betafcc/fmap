from typing import TypeVar, Iterable, Callable, Iterator
from .meta import Functor, MappedFunctor


A = TypeVar('A')
B = TypeVar('B')


class IterableFunctor(Functor[A], Iterable[A]):
    def __init__(self, source: Iterable[A]) -> None:
        self._source = source

    def fmap(self, f: Callable[[A], B]) -> 'MappedIterableFunctor[A, B]':
        return MappedIterableFunctor(f, self._source)

    def __iter__(self) -> Iterator[A]:
        return iter(self._source)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._source})'


class MappedIterableFunctor(MappedFunctor[A, B], Iterable[B]):
    _source: Iterable[A]

    def __iter__(self) -> Iterator[B]:
        return map(self._pipe, self._source)
