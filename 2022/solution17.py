from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np
import matplotlib.pyplot as plt
import itertools as itr


def draw(x,y,rocks, data,screen,max_height):
    rx,ry = zip(*sum([[(x,y) for y in ys] for x,ys in enumerate(rocks)],[]))
    data[ry,rx] = 5
    data[y,x]=10
    start = max(0,int(max_height)-3)
    screen.set_data(data[start:start+10])
    screen.set_extent([-0.5,7-0.5,start-0.5,start+9.5])
    plt.pause(0.5)
    data[y,x] = 0

def make_fast_moves(bmax):
    moves = {}
    for jets in itr.product(*[(-1,1)]*4):
        moves[jets] = 0
        for j in jets:
            if -3<moves[jets]+j<5-bmax:
                moves[jets]+=j
    return moves

def init_simulation():
    size=(3000,7)
    data = np.random.random(size)
    fig = plt.figure(figsize=(4.2,6))
    ax = fig.add_axes([0.1,0.1,0.9,0.9])
    screen = ax.imshow(data[:10], vmin = 0,vmax = 20,
            extent = [-0.5,7-0.5,-0.5,10-0.5], aspect="auto", cmap="gray",origin="lower")
    return data,screen

def can_move_here(bx,by,rocks):
    return not any(y in rocks[x] for x,y in zip(bx,by))

def solutions() -> Iterator[int]:
    jets = [1 if c==">" else -1 for c in get_puzzle_input(day=17, example=False, as_lines=False,).strip()]
    Lj = len(jets)
    bxs = [np.r_[0,1,2,3],np.r_[1,0,2,1],np.r_[0,1,2,2,2],np.r_[0,0,0,0],np.r_[0,1,0,1]]
    bys = [np.r_[0,0,0,0],np.r_[0,1,1,2],np.r_[0,0,0,1,2],np.r_[0,1,2,3],np.r_[0,0,1,1]]
    xmaxs = [3,2,2,0,1]
    ymaxs = [0,2,2,3,1]
    fast_moves = [make_fast_moves(xmax) for xmax in xmaxs]
    rocks = [{-1} for _ in range(7)]
    block_index = 0
    jet_index = 0
    bx0 = 2
    by0 = 0
    max_height = 0
    diffs = []
    diff_indices = {}
    sim = False
    N = 20
    for n_blocks in (2022,1_000_000_000_000):
        if sim:
            data,screen = init_simulation()
        while True:
            j_index = jet_index%Lj
            jet_index+=4
            b_index = block_index%5
            block_index+=1

            t = tuple(jets[j_index:j_index+4])
            if len(t)<4:
                t = t+tuple(jets[:(j_index+4)%Lj])
            dx = fast_moves[b_index][t]
            bx0+=dx
            bx = bxs[b_index]
            by = bys[b_index]
            xmax = xmaxs[b_index]
            ymax = ymaxs[b_index]
            if sim:
                draw(bx+bx0,by+by0,rocks,data,screen,max_height)
            while can_move_here(bx+bx0,by+by0-1,rocks):
                by0-=1
                jet = jets[jet_index%Lj]
                jet_index+=1

                if -1<bx0+jet<7-xmax:
                    if can_move_here(bx+bx0+jet,by+by0,rocks):
                        bx0+=jet
            if sim:
                draw(bx+bx0,by+by0,rocks,data,screen,max_height)
            for x,y in zip(bx+bx0,by+by0):
                rocks[x].add(y)

            max_height, last_max_height = max(max_height,by0+ymax+1),max_height
            new_diff = max_height - last_max_height
            diffs.append(new_diff)
            by0 = max_height
            bx0 = 2

            if len(diffs)>N:
                if (s:=tuple(diffs[-N:])) in diff_indices:
                    start_index = diff_indices[s]
                    period = block_index-start_index-N
                    repeated_seq = diffs[start_index:start_index+period]
                    div = (n_blocks-start_index)//period
                    mod = (n_blocks-start_index)%period
                    total_height = np.sum(diffs[:start_index], dtype=np.int64)\
                                 + div*np.sum(repeated_seq, dtype=np.int64)\
                                 + np.sum(repeated_seq[:mod], dtype=np.int64)
                    yield total_height
                    break
                else:
                    diff_indices[s] = block_index-N
        
show_answers(solutions)