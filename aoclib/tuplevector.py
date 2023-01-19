from typing import Iterable, Iterator, Union
import itertools as itr

class TupVec(tuple):

    def __new__ (cls, *args,**kwargs):
        if args and isinstance(args[0],Iterable):
            args = args[0]
        if isinstance(args,Iterator):
            args = list(args)
        if not args and "x" in kwargs and "y" in kwargs:
            args = kwargs.pop("x"), kwargs.pop("y")
        if len(args)==2 and "z" in kwargs:
            args = *args, kwargs.pop("z")
        return super(TupVec, cls).__new__(cls, tuple(args))

    def __getattr__(self, attr):
        return next(self[i] for i,c in enumerate("xyz") if c==attr)

    @property
    def ndim(self):
        return len(self)

    def __add__(self, translation:tuple[int,...]):
        return TupVec(p+t for p,t in itr.zip_longest(self,translation,fillvalue = 0))

    def __radd__(self, translation:tuple[int,...]):
        return self.__add__(translation)

    def __sub__(self, translation:tuple[int,...]):
        return TupVec(c-t for c,t in itr.zip_longest(self, translation, fillvalue=0))

    def __rsub__(self, translation:tuple[int,...]):
        return TupVec(t-c for c,t in itr.zip_longest(self, translation, fillvalue=0))

    def __mul__(self,factor:Union[int,tuple]):
        if isinstance(factor,int):
            factor = (factor,)*len(self)
        return TupVec(t*c for c,t in itr.zip_longest(self,factor, fillvalue=1))

    def __rmul__(self,factor:Union[int,tuple]):
        return self*factor

    def __neg__(self):
        return TupVec(-c for c in self)

    def neighbors(self, include_diagonals=False, only_diagonals=False) -> Iterator[tuple[int,...]]:
        if only_diagonals:
            for v in itr.product((0,-1,1), repeat=self.ndim):
                v_it = iter(v)
                if next((c for c in v_it if c),0) and next((c for c in v_it if c),0):
                    yield self + v
        elif include_diagonals:
            for i,v in enumerate(itr.product((0,-1,1), repeat=self.ndim)):
                if i:
                    yield self + v
        else:
            yield from (self+(sign*(i==j) for i in range(self.ndim)) for j in range(self.ndim) for sign in (-1,1))