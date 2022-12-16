from time import perf_counter as pc

def answer(L):
    with open("2022/input06.txt") as file:
        data = file.read()
        return next(i for i,chrs in enumerate(zip(*(data[shift:] for shift in range(L))), start=L) if len(set(chrs))==L)

t0=pc()
print(f"first marker occurs after position: {answer(4)}")
print(f"Message start after position: {answer(14)}")
print(f"Executed in time: {pc()-t0:.3f} s")