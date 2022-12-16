scores={"X":1,"Y":2,"Z":3,"A":1,"B":2,"C":3}


def score(opponent, you):
    s1=scores[opponent]
    s2=scores[you]
    gs=3*((s2-s1+1)%3)
    return s2+gs

tot_score=0
with open("2022/input02.txt") as file:
    for line in file:
        op, you = line.strip().split()
        tot_score += score(op, you)
            
print("Your total score =", tot_score)
