from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np
import matplotlib.pyplot as plt

def solutions() -> Iterator[int]:
    rock_paths = [[[int(x) for x in coord.split(",")] for coord in line.strip().split(" -> ")] \
                 for line in get_puzzle_input(day=14)]
    size = (200,750)
    cave_data = np.random.random(size)
    max_y = 0
    for rock_path in rock_paths:
        for (c1,r1),(c2,r2) in zip(rock_path,rock_path[1:]):
            r1,r2 = min(r1,r2),max(r1,r2)
            c1,c2 = min(c1,c2),max(c1,c2)
            max_y = max(max_y,r2)
            cave_data[r1:r2+1, c1:c2+1] = 5
    cave_data[max_y+2,:]=5
    fig,ax = plt.subplots()
    cave = ax.imshow(cave_data, vmin = 0,vmax = 20,
            extent = [-0.5,size[1]-0.5,size[0]-0.5,-0.5], aspect="auto", cmap="gray")
    ax.set_xlim(250, size[1])
    ax.set_ylim(200, -0.5)
    
    fixed_sand = set(zip(*np.where(cave_data>1)))
    init_size = len(fixed_sand)
    sand_motions = [(1,0),(1,-1),(1,1)]
    has_not_reached_the_floor = True
    moving_sand = [(0,500)]
    while moving_sand:
        while True:
            ys,xs = moving_sand[-1]
            cave_data[ys,xs] = 10
            for dy,dx in sand_motions:
                if (c:=(ys+dy,xs+dx)) in fixed_sand:
                    continue
                moving_sand.append(c)
                break
            else:
                fixed_sand.add(moving_sand.pop(-1))
                cave_data[ys,xs]=7
                if len(fixed_sand)%200==0:
                    cave.set_data(cave_data)
                    plt.pause(0.05)
                break
            if ys>=max_y and has_not_reached_the_floor:
                has_not_reached_the_floor = False
                yield len(fixed_sand)-init_size
    yield len(fixed_sand)-init_size
        
show_answers(solutions())