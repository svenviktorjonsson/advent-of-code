from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np
from collections import Counter

def solutions() -> Iterator[int]:
    coords = set(tuple(int(c) for c in line.strip().split(",")) for line in get_puzzle_input(day=18, example=False))
    shifts = np.r_[np.eye(3),-np.eye(3)].astype(int)
    counts = Counter([c for x,y,z in coords for dx,dy,dz in shifts if (c:=(x+dx,y+dy,z+dz)) not in coords])
    yield sum(counts.values())



    mins = np.min(list(zip(*coords)),axis=1).astype(int)
    maxs = np.max(list(zip(*coords)),axis=1).astype(int)
    xmi,ymi,zmi = mins
    outsiders = {(xmi-1,ymi-1,zmi-1)}
    iteration = 0
    visited = set()
    real_counts = {}
    while outsiders:
        coord = outsiders.pop()
        if coord in visited:
            continue
        visited.add(coord)
        iteration+=1
        # if iteration%100000==0:
        #     print("iter:",iteration,"nr of states",len(outsiders))
        if all(c>mi-2 for c,mi in zip(coord,mins)) and\
           all(c<ma+2 for c,ma in zip(coord,maxs)) and\
            coord not in coords:
            if coord in counts:
                real_counts[coord] = counts[coord]
            x,y,z = coord
            outsiders.update((x+dx,y+dy,z+dz) for dx,dy,dz in shifts)
    yield sum(real_counts.values())

show_answers(solutions)