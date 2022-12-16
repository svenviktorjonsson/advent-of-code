from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator

@dataclass
class Node:
    parent:Node = None
    _size:int = 0
    children:dict[str, Node] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return sum((node.size for node in self.children.values()), self._size)

def change_dir(parent:Node, dir_:str) -> Node:
    if dir_ == "..":
        return parent.parent
    return parent.children.setdefault(dir_, Node(parent))

def add_file(parent:Node, size:str, name:str) -> None:
    if not name in parent.children:
        file = Node(parent, int(size))
        parent.children[name] = file

def add_dir(parent:Node, name:str) -> None:
    parent.children.setdefault(name, Node(parent))

def get_nodes(parent:Node) -> Iterator[Node]:
    yield parent
    for child in parent.children.values():
        yield from get_nodes(child)

def read_row(parent:Node, row:str) -> Node:
    col1, col2, *args = row.split()
    if col1=="$":
        if col2 == "cd":
            return change_dir(parent, *args)
    elif col1 == "dir":
        add_dir(parent, col2)
    else:
        add_file(parent, col1, col2)
    return parent
        
with open("2022/input07.txt") as file:
    root = Node()
    parent = root
    for line in file:
        parent = read_row(parent, line.strip())


#question 1
dir_size_sum = sum(s for d in get_nodes(root) if d.children and (s:=d.size)<100000)
print(f"Sum of dir sizes unde 100 000: {dir_size_sum}")


#question 2 
need_to_remove = root.size - 40_000_000
min_removed_size = min(s for d in get_nodes(root) if d.children and (s:=d.size)>need_to_remove)
print(f"Minimum dir-size to remove: {min_removed_size}")


