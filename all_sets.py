import math
from metric import *

set_sizes = []
worst_set = []
worst_dist = 0

# plu[i] = proportion of voters who ranked candidate i first
# M[i][j] = proportion of voters who ranked i above j
plu, M = paper_ex()
# initialize weights w/ plurality count
weights = [int(x * m) for x in plu]

def likelihood(set):
    """ Calculates the proportion of voters with a given set of voters"""
    total = 0
    a, b, c = vals[m]
    if set[0] == 1 and set[m-1] == 2:
        if set[m-2] == 3:
            total = a * (1-c) / (a+b)
        elif set[1] == 3:
            total = a * (1 - (1-c) / (a+b))
    elif set[0] == 2 and set[m-1] == 1:
        if set[m - 2] == 3:
            total = b * (1 - c) / (a + b)
        elif set[1] == 3:
            total = b * (1 - (1 - c) / (a + b))
    elif set[0] == 3 and set[m-1] == 1 and set[m-2] == 2:
        total = 1 - (a + b)
    return total / math.factorial(m-3)

def assess(I):
    """ Gets the ratio for a given set I """
    # numerator
    for j in range(1, m+1):
        if j in I:
            continue


def explore_all(curr = []):
    """ Recursively runs through all possible sets of I and find the worst one """
    if len(curr) == m:
        return
    # ordering matters
    for i in range(1, m+1):
        if i in curr:
            continue
        next = curr + [i]
        # assess the ratio
        explore_all(next)

if __name__ == "__main__":
    print(likelihood([1, 4, 3, 2]))