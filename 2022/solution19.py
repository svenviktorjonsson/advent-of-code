from __future__ import annotations
from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import numpy as np
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
import re
from operator import add

@dataclass(frozen = True)
class State:
    time_left : int
    resources : tuple[int, ...]
    robots : tuple[int, ...]

    def min_geode(self):
        return self.resources[-1]+self.time_left*self.robots[-1]

    def potential(self,values):
        return sum(v*(res+rob*self.time_left) for v,res,rob in zip(values,self.resources,self.robots))
    
    def can_buy(self,cost):
        return all(self.resources[res]>=c for res,c in cost.items())

    def valid_option(self,robot,costs,options):
        if robot==0 and self.time_left-1<costs[0]:
            return False
        robots,costs = zip(*options)
        if 3 in robots and robot!=3:
            return False
        return True

    def future_states(self, blueprint:dict) -> Iterator[State]:
        options = [(res,costs) for res,costs in enumerate(blueprint) if self.can_buy(costs)]
        for robot,costs in options:
            if not self.valid_option(robot, costs, options):
                continue
            new_resources = tuple(Nres+Nrob-costs.get(res,0) for res,(Nres,Nrob) in enumerate(zip(self.resources,self.robots)))
            new_robots = list(self.robots)
            new_robots[robot]+=1
            yield State(self.time_left-1, new_resources, tuple(new_robots))
        new_resources = tuple(map(add,self.resources,self.robots))
        yield State(self.time_left-1, new_resources, self.robots)


def solutions() -> Iterator[int]:
    data = [[int(d.strip(":")) for d in line.split() if d.strip(":").isdigit()] for line in get_puzzle_input(day=19, example=True)]
    
    blueprints = [(d[0],({0:d[1]},{0:d[2]},{0:d[3],1:d[4]},{0:d[5],2:d[6]}),
                        (1,d[2],d[3]+d[2]*d[4],d[5]+(d[3]+d[2]*d[4])*d[6])) for d in data]
    for n,time in [(len(blueprints),24),(3,32)][:1]:
        quality_level = 0
        product = 1
        for ID,blueprint,values in blueprints[:n]:
            states = [State(time,(0,0,0,0),(1,0,0,0))]
            max_geodes = 0
            visited = set()
            while states:
                if len(states)>5000:
                    states.sort(key = lambda s:-s.potential(values))
                    states = states[:500]
                state = states.pop(0)
                if state in visited:
                    continue
                visited.add(state)
                max_geodes = max(max_geodes,state.min_geode())
                if state.time_left<2:
                    continue
                states.extend(state.future_states(blueprint))
            print(max_geodes)
            product*=max_geodes
            quality_level+=max_geodes*ID
        if n>3:
            yield quality_level
        else:
            yield product

show_answers(solutions)