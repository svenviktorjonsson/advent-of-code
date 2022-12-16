
def badge(items:str) -> str:
    return set.intersection(*items).pop()


def priorities(item_type:str):
    code = ord(item_type)
    return code-96 if code>96 else code-38


with open("2022/input03.txt") as file:
    item_sets = [set(line.strip()) for line in file]
    badges = [badge(item_sets[i*3:(i+1)*3]) for i in range(len(item_sets)//3)]


result = sum(map(priorities, badges))

print(f"Sum of badge priorities: {result}")

