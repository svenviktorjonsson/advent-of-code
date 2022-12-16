import numpy as np
from typing import Iterator
import matplotlib.pyplot as plt
from collections import defaultdict
import time

from aoclib import show_answers, get_puzzle_input

def find_shorted_path(terrain, start, end, going_up=True):
    paths = [[start]]
    terrain[start][0] = True
    while paths:
        path = paths.pop(0)
        for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
            x,y = path[-1]
            new_pos = (x+dx,y+dy)
            _,from_height = terrain[(x,y)]
            visited, to_height = terrain.get(new_pos,[True,''])
            if visited or ((ord(to_height)>ord(from_height)+1) if going_up 
                      else (ord(from_height)>ord(to_height)+1)):
                continue
            if new_pos == end or terrain[new_pos][1] == end:
                return path+[new_pos]
            terrain[new_pos][0] = True
            paths.append(path.copy()+[new_pos])

def solutions() -> Iterator[int]:
    terrain = {}
    data = get_puzzle_input(day=12)
    for y,line in enumerate(data):
        for x,height in enumerate(line.rstrip()):
            if height == "S":
                start = (x,y)
                height = "a"
            elif height == "E":
                end = (x,y)
                height = "z"
            terrain[(x,y)] = [False,height]
    shortest_path = find_shorted_path(terrain, start, end, going_up=True)
    yield len(shortest_path)-1

    for k,v in terrain.items():
        v[0] = False
    shortest_hike = find_shorted_path(terrain, end, 'a', going_up=False)
    yield len(shortest_hike)-1

show_answers(solutions())