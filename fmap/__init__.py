from typing import Callable, Iterable, Sequence, TypeVar, overload
from .meta import Functor
from .sequence import SequenceFunctor, MappedSequenceFunctor
from .iterable import IterableFunctor, MappedIterableFunctor


A = TypeVar('A')
B = TypeVar('B')


@overload
def fmap(f: Callable[[A], B], fa: Functor[A]) -> Functor[B]:
    ...


@overload
def fmap(f: Callable[[A], B], it: Iterable[A]) -> MappedIterableFunctor[A, B]:
    ...


@overload
def fmap(f: Callable[[A], B], seq: Sequence[A]) -> MappedSequenceFunctor[A, B]:
    ...


def fmap(f, it):  # type: ignore
    try:
        return it.fmap(f)

    except AttributeError:
        if isinstance(it, Sequence):
            return SequenceFunctor(it).fmap(f)

        elif isinstance(it, Iterable):
            return IterableFunctor(it).fmap(f)

        raise TypeError(f"Can't fmap type {type(it)}")
