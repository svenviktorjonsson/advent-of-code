
def common_char(line:str):
    L = len(line)//2
    sets= set(line[:L]),set(line[L:])
    return set.intersection(*sets).pop()

def priorities(item_type:str):
    code = ord(item_type)
    return code-96 if code>96 else code-38

with open("input03.txt") as file:
    data = [common_char(line.strip()) for line in file]
        
result = sum(map(priorities,data))
        

print(f"Sum of priorities: {result}")

