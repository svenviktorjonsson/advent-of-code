from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np

def solutions() -> Iterator[int]:
    data = [[[d.strip(", y") for d in info.split("=")[1:]] for info in line.split(":")]\
            for line in get_puzzle_input(day = 15)]
    data = np.array(data,dtype=int)
    #data shape: (input row,[sensor (s),beacon (b)],[x,y])
    
    roi = 2_000_000 #row of interest
    s_b_dist = np.sum(np.abs(np.diff(data,axis=1)),axis=(1,2))
    s_roi_dist = np.abs(data[:,0,1] - roi)
    bx_sx_dists_on_roi = s_b_dist - s_roi_dist
    bx,by = data[:,1,:].T
    near_roi = bx_sx_dists_on_roi>=0
    bx_sx_dists_on_roi = bx_sx_dists_on_roi[near_roi]
    sx = data[near_roi,0,0]
    ranges = np.concatenate([np.arange(x-dist,x+dist+1) for x,dist in zip(sx,bx_sx_dists_on_roi)])
    yield np.setdiff1d(ranges,bx[by==roi]).size

    limit = 4_000_000
    first_diag = -1j-1
    rotations = 1j**np.arange(4)[None,None,:]
    sensors = data[:,0,0]+1j*data[:,0,1]
    perims = [(sensor + (dist+1+np.arange(dist+1)[:,None]*first_diag)*rotations).flat \
              for sensor,dist in zip(sensors,s_b_dist)]

    perims = np.concatenate(perims)
    inside_square = (np.abs(np.real(perims)-limit//2)<=limit//2) \
                  * (np.abs(np.imag(perims)-limit//2)<=limit//2)
    
    perims,counts = np.unique(perims[inside_square],return_counts=True)
    perims = perims[counts>1]

    for sensor, dist in zip(sensors,s_b_dist):
        diff = perims - sensor
        pdist = np.abs(diff.real) + np.abs(diff.imag)
        perims = perims[pdist>dist]
    zb, = perims
    yield int(zb.real*4_000_000 + zb.imag)
        
show_answers(solutions())