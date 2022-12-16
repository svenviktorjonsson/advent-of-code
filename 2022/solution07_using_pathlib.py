from pathlib import Path
from collections import defaultdict
from aoclib import get_puzzle_input

def parse_tokens(tokens:list[str], cwd:Path, files:list[Path]) -> Path:
    if tokens[0]=="$":
        if tokens[1]=="cd":
            cwd = (cwd / tokens[2]).resolve()
    elif tokens[0]!="dir":
        key = str(cwd / tokens[1]).strip("C:")
        files[key] = int(tokens[0])
    return cwd

data = [line.split() for line in get_puzzle_input(day=7)]

cwd = Path("")
files = {}

for tokens in data:
    cwd = parse_tokens(tokens, cwd, files)

dir_sizes = defaultdict(int)
total_size = 0
for path, size in files.items():
    while (path:=path.rsplit("\\",1)[0]):
        dir_sizes[path]+=size
    total_size+=size

result1 = sum(s for s in dir_sizes.values() if s<100000)
print("answer 1:", result1)

size_to_remove = total_size - 40_000_000
result2 = min(s for s in dir_sizes.values() if s>size_to_remove)
print("answer 2:", result2)