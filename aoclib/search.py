
from collections import deque
from typing import Iterator,Any,Callable

def bfs(init,get_next,keep):
    """Breadth first search"""
    states = deque([init])
    while states:
        state = states.pop()
        if not keep(state):
            continue
        yield state
        for next_state in get_next(state):
            states.append(next_state)

def dfs(init:Any,get_next:Callable,keep:Callable) -> Iterator[Any]:
    """Depth first search
    
    Prunes away branches
    """
    states = deque([init])
    while states:
        state = states.popleft()
        if not keep(state):
            continue
        yield state
        for next_state in get_next(state):
            states.appendleft(next_state)

