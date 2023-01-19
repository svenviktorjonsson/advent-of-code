from time import perf_counter

from typing import Iterator

def show_answers(solutions:Iterator) -> None:
    t0 = perf_counter()
    if (s:=solutions()) is not None:
        for i, answer in enumerate(s, start=1):
            print(f"Answer {i}:\n{answer}\n")
    print(f"Executed in {perf_counter()-t0:.6f} s")