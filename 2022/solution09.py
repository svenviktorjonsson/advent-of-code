from time import perf_counter
import re
import numpy as np

from typing import Iterator


def parse_input() -> list[list[int]]:
    with open("2022/input09.txt") as file:
        return [re.search("(\w) (\d+)", line).groups() for line in file]


def move_rope(rope:list[tuple[int,int]], 
              dx_hare:int, dy_hare:int) -> None:
    for knot_index, (xi,yi) in enumerate(rope):
        xlead, ylead = rope[knot_index-1] if knot_index \
                       else (xi+dx_hare, yi+dy_hare) 
        if abs(xlead-xi)>1 or abs(ylead-yi)>1:
            rope[knot_index] = xi + np.sign(xlead-xi),\
                               yi + np.sign(ylead-yi)
        else: break


def solutions() -> Iterator[int]:
    cmds = parse_input()
    hare_motion = {"R":(2,0), "L":(-2,0), "U":(0,2), "D":(0,-2)}
    for N in (2, 10):
        visited_points = {(0,0)}
        rope = [(0,0)]*N
        for direction, steps in cmds:
            for _ in range(int(steps)):
                move_rope(rope, *hare_motion[direction])
                visited_points.add(rope[N-1])
        yield len(visited_points)


answer = solutions()

t0 = perf_counter()
print("Answer 1:", next(answer))
print("Answer 2:", next(answer))
print(f"Executed in {perf_counter()-t0:.3f} s")