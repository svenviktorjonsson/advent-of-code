
with open("2022/input04.txt") as file:
    data = [line.strip().split(",") for line in file]

def contains(rangs):
    mi1, ma1 = map(int, rangs[0].split("-"))
    mi2, ma2 = map(int, rangs[1].split("-"))
    return mi2>=mi1 and ma2<=ma1 or mi1>=mi2 and ma1<=ma2

print(f"result: {sum(map(contains,data))}")

