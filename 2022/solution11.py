from time import perf_counter
import math

from typing import Iterator, Any

def parse_section(section:str) -> tuple[int,tuple]:
    data = [line.split(":")[-1] for line in section.split("\n")[1:]]
    items = [int(item) for item in data[0].split(",")]
    op,factor = data[1].split()[-2:]
    mod,if_true,if_false = [int(d.split()[-1]) for d in data[2:]]
    return [0, items, factor, op, mod, if_true, if_false]

def parse_input() -> list[list[int]]:
    with open("2022/input11.txt") as file:
        return [parse_section(s) for s in file.read().split("\n\n")]

def solutions() -> Iterator[int]:
    for div,rounds in [(3,20),(1,10000)]:
        monkeys = parse_input()
        *_,mods,_,_ = zip(*monkeys)
        for _ in range(rounds):
            for index, (activity, items, factor, op, mod, if_true, if_false) in enumerate(monkeys):
                monkeys[index][0]+=len(items)
                while items:
                    old = items.pop(0)
                    expr = f"old {op} {factor}"
                    new_worry = eval(expr)%math.prod(mods)//div
                    to = if_false if new_worry%mod else if_true
                    monkeys[to][1].append(new_worry)
        activity,*_ = zip(*monkeys)
        x,y = sorted(activity)[-2:]
        yield x*y



answer = solutions()

t0 = perf_counter()
print("Answer 1:", next(answer))
print("Answer 2:", next(answer))
print(f"Executed in {perf_counter()-t0:.3f} s")