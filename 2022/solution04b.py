import itertools as itr
import numpy as np

with open("2022/input04.txt") as file:
    data = [line.strip().split(",") for line in file]

def overlap(rangs):
    mi1, ma1 = map(int,rangs[0].split("-"))
    mi2, ma2 = map(int,rangs[1].split("-"))
    set1 = set(range(mi1, ma1+1))
    set2 = set(range(mi2, ma2+1))
    return bool(set1.intersection(set2))

print(f"result: {sum(map(overlap, data))}")

