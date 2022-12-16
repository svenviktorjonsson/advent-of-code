
with open("2022/input05.txt") as file:
    crates_data,cmds_data = file.read().split("\n\n")
    crates = [[ci.strip("[]") for ci in c[:-1] if ci] for c in 
            zip(*([row[4*i:4*(i+1)].strip() for i,_ in enumerate(row[::4])] 
            for row in crates_data.split("\n")))]
    cmds = [[int(token) for token in line.strip().split() if token.isdigit()] 
            for line in cmds_data.split("\n")]

for amount,src,dest in cmds:
    for i in range(amount):
        crates[dest-1].insert(i,crates[src-1].pop(0))

top_crates = "".join([c[0] for c in crates])
print(f"Top crates: {top_crates}")