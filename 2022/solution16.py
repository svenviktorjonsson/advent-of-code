from typing import Iterator

from aoclib import show_answers, get_puzzle_input
import re

def solutions() -> Iterator[int]:
    pattern = "Valve (?P<name>\w\w).*rate\=(?P<rate>\d+).*valves? (?P<to>.*)"
    data = {(g:=re.search(pattern,line).groupdict())["name"]:g for line in get_puzzle_input(day=16,example=True)}
    
    time = 30
    
    
    yield 0
        
show_answers(solutions())