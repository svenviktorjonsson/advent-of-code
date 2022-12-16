cals_count=0
max_cals=0

with open("2022/input01.txt") as file:
    for line in file:
        cals=line.strip()
        if cals:
            cals_count+=int(cals)
        else:
            cals_count, max_cals = 0, max(max_cals, cals_count)
print("max calories =",max_cals)
