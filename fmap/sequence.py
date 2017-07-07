from typing import TypeVar, Sequence, Callable, overload, Union, Iterator
from .meta import Functor, MappedFunctor


A = TypeVar('A')
B = TypeVar('B')


class SequenceFunctor(Sequence[A], Functor[A]):
    def __init__(self, source: Sequence[A]) -> None:
        self._source = source

    def fmap(self, f: Callable[[A], B]) -> 'MappedSequenceFunctor[A, B]':
        return MappedSequenceFunctor(f, self._source)

    def __len__(self) -> int:
        return len(self._source)

    @overload
    def __getitem__(self, index: int) -> A:
        ...

    @overload
    def __getitem__(self, slice: slice) -> 'SequenceFunctor[A]':
        ...

    def __getitem__(self,  # type: ignore
                    query: Union[int, slice]
                    ) -> Union[A, 'SequenceFunctor[A]']:
        if isinstance(query, int):
            return self._source[query]
        elif isinstance(query, slice):
            return SequenceFunctor(self._source[query])
        else:
            raise TypeError(
                'fmap only supports int and slice for indexing'
            )


class MappedSequenceFunctor(MappedFunctor[A, B], Sequence[B]):
    _source: Sequence[A]

    def __len__(self) -> int:
        return len(self._source)

    def __iter__(self) -> Iterator[B]:
        return map(self._pipe, self._source)

    @overload
    def __getitem__(self, index: int) -> B:
        ...

    @overload
    def __getitem__(self, slice: slice) -> 'MappedSequenceFunctor[A, B]':
        ...

    def __getitem__(self,  # type: ignore
                    query: Union[int, slice]
                    ) -> Union[B, 'MappedSequenceFunctor[A, B]']:
        if isinstance(query, int):
            return self._pipe(self._source[query])
        elif isinstance(query, slice):
            return MappedSequenceFunctor(self._pipe, self._source[query])
        else:
            raise TypeError(
                'fmap only supports int and slice for indexing'
            )
