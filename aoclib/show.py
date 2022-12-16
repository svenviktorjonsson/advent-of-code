from time import perf_counter

def show_answers(solutions):
    t0 = perf_counter()
    for i, answer in enumerate(solutions, start=1):
        print(f"Answer {i}:\n{answer}\n")
    print(f"Executed in {perf_counter()-t0:.4f} s")