cals_count=0
max_cals=[]

with open("2022/input01.txt") as file:
    for line in file:
        cals=line.strip()
        if cals:
            cals_count+=int(cals)
        else:
            max_cals=sorted(max_cals+[cals_count])[-3:]
            cals_count=0          
print("max calories =",sum(max_cals))
