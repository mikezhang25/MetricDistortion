import numpy as np
import matplotlib.pyplot as plt

# number of candidates
m = 4
step_size = .1

# paper example matrix
vals = {3 : [0.473356, 0.423961, 0],
        4 : [0.459994, 0.406749, 0.363254],
        5 : [0.452953, 0.400474, 0.373050],
        10: [0.440434, 0.392546, 0.387236]}

# randomly initialize comparisons matrix and plurality vector
def random_init():
    # randomly generated proportions
    vec = np.random.dirichlet(np.ones(m), size=1)[0]

    matrix = [[0 for _ in range(m)] for __ in range(m)]
    # make sure that it's complementary across diagonal
    for i in range(m):
        for j in range(i + 1, m):
            matrix[i][j] = np.random.uniform()
            matrix[j][i] = 1 - matrix[i][j]
    return vec, matrix

def easy_ex():
    vec = [0] + [1 / (m - 1) for _ in range(m - 1)]

    matrix = [[0 for _ in range(m)] for __ in range(m)]
    # make sure that it's complementary across diagonal
    for i in range(1, m):
        matrix[0][i] = (m - 2) / (m - 1)
        matrix[i][0] = 1 - matrix[0][i]
    for i in range(1, m):
        for j in range(i + 1, m):
            matrix[i][j] = 1 / 2
            matrix[j][i] = 1 - matrix[i][j]
    return vec, matrix

def paper_ex():
    # constant values [a, b, c, 0.5, ...]
    val = vals[m] + [1 / 2 for _ in range(m - 3)]

    vec = [val[0], val[1], 1 - (val[0] + val[1])] + [0 for _ in range(m - 3)]
    matrix = [[0 for _ in range(m)] for __ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            matrix[i][j] = val[i]
            matrix[j][i] = 1 - matrix[i][j]

    return vec, matrix

""" Calculate the social cost for candidate j given metric i"""
def sc(j, i, plu, M):
    if i == j:
        # distortion for candidate i = # voters who didn't vote for i first
        return 1 - plu[i]

    # voters ranking j over i, so distance from i to voter (1 cuz not plurality)
    cost = M[j][i]
    # voters ranking i first (i over j), so distance 2
    cost += 2 * plu[i]
    # voters ranking i over j but not i first
    cost += 3 * (M[i][j] - plu[i])
    return cost


""" Calculates the distortion for a given metric i and weights w"""
def distortion(i, w, plu, M):
    e_sc = 0
    min_sc = float('inf')
    # normalize weights
    w_norm = [x / sum(w) for x in w]

    for c in range(m):
        cost = sc(c, i, plu, M)
        e_sc += w_norm[c] * cost
        min_sc = min(cost, min_sc)
    return e_sc / min_sc