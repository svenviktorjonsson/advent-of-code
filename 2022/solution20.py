from typing import Iterator

from aoclib import show_answers, get_puzzle_input

def move_element(index:int, data:list[tuple[int,int]]) -> None:
    item = data.pop(index)
    new_index = (index+item[1]%len(data))%len(data)
    data.insert(new_index,item)

def mix_elements(data) -> None:
    for d_index in range(len(data)):
        index = next(i for i,(index,d) in enumerate(data) if index==d_index)
        move_element(index,data)

def solutions() -> Iterator[int]:
    data = list(map(int,get_puzzle_input(day=20, example=False)))
    for factor,mix_count in [(1,1),(811589153,10)]:
        new_data = [(index,value*factor) for index,value in enumerate(data)]
        for _ in range(mix_count): mix_elements(new_data)
        zero_index = next(i for i,(_,d) in enumerate(new_data) if not d)
        yield sum(new_data[(zero_index+i)%len(new_data)][1] for i in (1000,2000,3000))

show_answers(solutions)
