from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import math
import functools as fts

from typing import Union

def cmp(left:Union[int,list], right:Union[int,list]) -> int:
    left_is_int = isinstance(left, int)
    if left_is_int ^ isinstance(right, int):
        left, right = ([left], right) if left_is_int else (left, [right])
    elif left_is_int:
        return (right<left) - (left<right)
    cmps = (c for p in zip(left, right) if (c := cmp(*p)))
    return next(cmps, cmp(len(left),len(right)))


def solutions() -> Iterator[int]:
    raw = get_puzzle_input(day=13, as_lines=False)
    data = [eval(section.replace("\n",",")) for section in raw.strip().split("\n\n")]
    yield sum([i for i,pair in enumerate(data, start=1) if cmp(*pair)<=0])

    div_ps = ([[2]], [[6]])
    ps = sum(data,()) + div_ps
    ord_ps = sorted(ps, key=fts.cmp_to_key(cmp))
    yield math.prod(i for i,p in enumerate(ord_ps, start=1) if p in div_ps)

show_answers(solutions())