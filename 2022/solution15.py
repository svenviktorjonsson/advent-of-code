from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np

def solutions() -> Iterator[int]:
    row_of_interest = 2_000_000
    data = np.array([[[int(data.strip(", y")) for data in info.split("=")[1:]] for info in line.split(":")] for line in get_puzzle_input(day = 15)])
    #data = (enumeration,kind,axis)
    s_to_b = np.sum(np.abs(np.diff(data,axis=1)),axis=(1,2))
    s_to_2m = np.abs(data[:,0,1]-row_of_interest)
    bx_min_dists = s_to_b-s_to_2m
    of_interest = bx_min_dists>=0
    bx_on_2m = set(data[:,1,0][data[:,1,1]==row_of_interest])
    
    sx = data[:,0,0]
    bx_min_dists = bx_min_dists[of_interest]
    sx = sx[of_interest]
    impossible_bx = set.union(*(set(range(sxi-bmin_dist,sxi+bmin_dist+1)) for sxi,bmin_dist in zip(sx,bx_min_dists)))
    yield len(impossible_bx-bx_on_2m)

    
        
show_answers(solutions())