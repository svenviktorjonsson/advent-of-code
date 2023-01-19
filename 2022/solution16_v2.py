from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import re
from collections import defaultdict
from time import perf_counter as pc
from dataclasses import dataclass,replace,field

@dataclass(frozen=True)
class Agent:
    time_left : int
    current_valve : str

@dataclass(frozen=True)
class State:
    pressure_release : int
    open_valves : frozenset
    agents : tuple[Agent]

def solutions() -> Iterator[int]:

    pattern = "Valve (?P<at>\w\w).*rate\=(?P<rate>\d+).*valves? (?P<to>.*)"
    data = {(g:=re.search(pattern,line).groupdict())["at"]:(int(g["rate"]),frozenset([n.strip() for n in g["to"].split(",")])) \
            for line in get_puzzle_input(day=16,example=False)}

    paths = defaultdict(list)
    visits = defaultdict(set)
    trs = [("AA","AA")]
    rates = {k:r for k,(r,_) in data.items()}
    while trs:
        tr = trs.pop(0)
        for to_valve in data[tr[1]][1]:
            next_tr = tr[0],to_valve
            if tr[0]==to_valve or to_valve in visits[tr[0]]:
                continue
            visits[tr[0]].add(to_valve)
            if tr in paths and not next_tr in paths:
                paths[next_tr] = paths[tr] + [tr[1]]
            elif tr[0]==tr[1]:
                paths[next_tr] = []
            trs.append((to_valve,)*2)
            trs.append(next_tr)
    distancies = {(v1,v2):len(v)+1 for (v1,v2),v in paths.items() if rates[v2] and (rates[v1] or v1=="AA")}
    
    iterations = 0
    init_part1 = set([(0,frozenset({"AA"}),((30,"AA"),))])
    init_part2 = set([(0,frozenset({"AA"}),((26,"AA"),(26,"AA")))])
    for states in init_part1,:#,init_part2:
        t0=pc()
        max_pressure = 0
        while states:
            iterations+=1
            pr, open_valves, agents = states.pop()
            valves = set(rates.keys())-open_valves
            while valves:
                to_valve = valves.pop()
                info = []
                for i, (tl,from_valve) in enumerate(agents):
                    tr = from_valve, to_valve
                    if tr not in distancies:
                        continue
                    dist = distancies[tr]
                    rate = rates[to_valve]
                    new_tl = tl - dist - 1
                    if new_tl<=0:
                        continue
                    new_pr = pr + rate*new_tl
                    new_open_valves = open_valves.union({to_valve})
                    info.append((new_tl,new_pr,new_open_valves,to_valve,i))
                if info:
                    new_tl,new_pr,new_open_valves,to_valve,index = max(info)
                    new_agents = tuple(sorted((new_tl,to_valve) if i==index else a for i,a in enumerate(agents)))
                    states.add((new_pr,new_open_valves,new_agents))
                    if new_pr>max_pressure:
                        max_pressure = new_pr
            if iterations%100000==0:
                print(max_pressure,f"time: {pc()-t0:.2f}, iter: {iterations}, states: {len(states)}")
        yield max_pressure
        
show_answers(solutions)