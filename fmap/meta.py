from typing import Generic, TypeVar, Callable, Iterable
from abc import ABCMeta, abstractmethod
from .util import compose


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
E = TypeVar('E')


class Functor(Generic[A], metaclass=ABCMeta):
    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        ...

    def __or__(self, other: Callable[[A], B]) -> 'Functor[B]':
        return self.fmap(other)

    # def __rshift__(self, other: B) -> 'Functor[B]':
    #     return self.fmap(const(other))

    # def __lshift__(self, other: 'Functor[B]') -> 'Functor[Functor[A]]':
    #     return other >> self

    # def __rlshift__(self, other: B) -> 'Functor[B]':
    #     return self >> other


class MappedFunctor(Generic[A, B], Functor[B]):
    def __init__(self,
                 pipe   : Callable[[A], B],
                 source : Iterable[A],
                 ) -> None:
        # The sinfull protected attributes
        self._pipe   = pipe
        self._source = source

    @classmethod
    def from_mapped(cls,
                    f: Callable[[D], E],
                    source: 'MappedFunctor[C, D]',
                    ) -> 'MappedFunctor[C, E]':
        new_pipe = compose(f, source._pipe)
        return cls(new_pipe, source._source)

    def fmap(self, f: Callable[[B], C]) -> 'MappedFunctor[A, C]':
        return self.from_mapped(f, self)

    def __repr__(self) -> str:
        try:
            return f'fmap({self._pipe.__name__}, {repr(self._source)})'
        except AttributeError:
            return f'fmap({repr(self._pipe)}, {repr(self._source)})'
