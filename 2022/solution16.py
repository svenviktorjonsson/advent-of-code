from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import re
from collections import defaultdict
import itertools as itr

# def add_distance(distancies,visits,from_valve,to_valves, data, dist=0):
#     next_valvess = []
#     for to_valve in to_valves:
#         if to_valve in visits:
#             continue
#         visits.add(to_valve)
#         pair = frozenset((from_valve,to_valve))
#         rate, next_valves = data[to_valve]
#         if 
#         distancies[pair] = dist+1
#         next_valvess.append(next_valves)
#     for next_valves in next_valvess:
#         add_distance(distancies,visits,from_valve,next_valves,data,dist+1)

# def pressure(route, rates, distancies):
#     total_pressure = 0
#     time_left = 30
#     for tr in zip(route,route[1:]):
#         dist = distancies.get(tr) or distancies.get(tr[::-1])
#         time_left-=dist+1
#         if time_left>0:
#             total_pressure += rates[tr[1]]*time_left
#         else:
#             time_left=0
#             break
#     return total_pressure, time_left

def solutions() -> Iterator[int]:

    pattern = "Valve (?P<at>\w\w).*rate\=(?P<rate>\d+).*valves? (?P<to>.*)"
    data = {(g:=re.search(pattern,line).groupdict())["at"]:(int(g["rate"]),frozenset([n.strip() for n in g["to"].split(",")])) \
            for line in get_puzzle_input(day=16,example=True)}

    visits = defaultdict(set)
    distancies = {}
    positions = [(0,"AA","AA")]
    rates = {k:r for k,(r,_) in data.items()}
    while positions:
        length, from_valve, valve = positions.pop(0)
        for to_valve in data[valve][1]:
            if from_valve==to_valve or to_valve in visits[from_valve]:
                continue
            visits[from_valve].add(to_valve)
            tr = (from_valve,to_valve)
            rate = data[to_valve][0]
            if tr not in distancies and rate:
                distancies[tr] = length+1
            positions.append((length+1,from_valve,to_valve))
            if rate:
                positions.append((0,to_valve,to_valve))
    
    for k,v in sorted(distancies.items()):
        print(k,v)
    return None
    
    for states in ([(0,(26,["AA"]),(26,["AA"]))],):
        max_pressure = 0
        while states:
            states.sort()
            pr,*agents = states.pop(-1)
            if all(tl<=0 for tl,path in agents):
                continue
            valves = list(rates.keys())
            while valves:
                to_valve = valves.pop(0)
                info = []
                visited = set.union(*(set(p) for _,p in agents))
                for i,(tl,path) in  enumerate(agents):
                    from_valve = path[-1]
                    tr = from_valve,to_valve
                    if (dist:=distancies.get(tr,0))==0 or to_valve in visited:
                        continue
                    rate = rates[to_valve]
                    new_tl = tl - dist - 1
                    new_pr = pr + rate*new_tl
                    new_path = path+[to_valve]
                    info.append((new_tl,new_pr,new_path,i))
                if not info:
                    continue
                new_tl,new_pr,new_path,index = max(info)
                new_agents = agents.copy()
                new_agents[index] = new_tl,new_path
                new_state = (new_pr,)+tuple(new_agents)
                # print(new_state)
                states.append(new_state)
                if new_pr>max_pressure:
                    max_pressure = new_pr
                    print(max_pressure)
        yield max_pressure
        
show_answers(solutions)