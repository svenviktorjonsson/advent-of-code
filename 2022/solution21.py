from typing import Iterator

from aoclib import show_answers, get_puzzle_input
from operator import add,sub,mul,truediv
import re
operators = {"+":add,"-":sub,"*":mul,"/":truediv,None:(lambda x,_:x)}

def evaluate(data,key):
    if isinstance(data[key],(int,float)):
        return data[key]
    op,(first,second) = data[key]
    return op(evaluate(data,first),evaluate(data,second))

def solutions() -> Iterator[int]:
    pattern = r"(?P<key>\w+): (?P<first>\w+)\s?(?P<op>[\+\-\*/])?\s?(?P<second>\w+)?"
    raw_data = [re.search(pattern,line).groupdict() for line in get_puzzle_input(year=2022,day=21, example=False)]

    data = {d["key"]:int(d["first"]) if d["first"].isdigit() else (operators[d["op"]],(d["first"],d["second"])) for d in raw_data}
    yield int(evaluate(data,"root"))

    data["root"] = (lambda x,y:x-y, data["root"][1])
    data["humn"] = 1
    root = evaluate(data,"root")
    factor=2
    while abs(root:=evaluate(data,"root"))>1e-4:
        if root<0:
            data["humn"] /= factor
            factor**=0.5
        else:
            data["humn"] *= factor
        
    yield int(data["humn"]+0.5)

show_answers(solutions)
