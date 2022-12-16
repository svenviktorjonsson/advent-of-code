from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np

def solutions() -> Iterator[int]:
    rock_paths = [[list(map(int, coord.split(","))) for coord in line.split(" -> ")] \
                 for line in get_puzzle_input(day=14)]
    size = (200,750)
    cave_data = np.full(size,False)
    y_max = 0
    for rock_path in rock_paths:
        for (c1,r1),(c2,r2) in zip(rock_path,rock_path[1:]):
            (r1,r2),(c1,c2) = sorted((r1,r2)),sorted((c1,c2))
            y_max = max(y_max,r2)
            cave_data[r1:r2+1, c1:c2+1] = True
    cave_data[y_max+2,:]=True
    obsticles = set(zip(*np.where(cave_data)))
    init_size = len(obsticles)
    sand_motions = [(1,0),(1,-1),(1,1)]
    has_not_reached_the_floor = True
    moving_sand = [(0,500)]
    while moving_sand:
        while True:
            ys,xs = moving_sand[-1]
            for dy,dx in sand_motions:
                if not (c:=(ys+dy,xs+dx)) in obsticles:
                    moving_sand.append(c)
                    break
            else:
                obsticles.add(moving_sand.pop(-1))
                break
            if ys>=y_max and has_not_reached_the_floor:
                has_not_reached_the_floor = False
                yield len(obsticles)-init_size
    yield len(obsticles)-init_size
        
show_answers(solutions())