# Copyright 2022, Gurobi Optimization, LLC

# This example formulates and solves the following simple bilinear model:
#  maximize    x
#  subject to  x + y + z <= 10
#              x * y <= 2         (bilinear inequality)
#              x * z + y * z = 1  (bilinear equality)
#              x, y, z non-negative (x integral in second version)
from math import factorial
import itertools
import gurobipy as gp
from gurobipy import GRB, LinExpr

# CONSTANTS
M = 4
U = {i for i in range(1, M+1)}

# SETUP MODEL
# Create a new model
model = gp.Model("bilinear")

# generate all possible sets I
sets = []
def generate_sets(curr = []):
    if 0 < len(curr) < M:
        sets.append({i for i in curr})
    for i in range(1, M+1):
        if len(curr) == 0 or i > curr[len(curr)-1]:
            generate_sets(curr + [i])

# all possible election instances
all_perms = list(itertools.permutations([i for i in range(1, M+1)]))

def hash(set, i):
    hash = i
    for val in set:
        hash *= 10
        hash += val
    return hash

def eval(ordering, A, B):
    A_max = max([ordering.index(a) for a in A])
    B_min = min([ordering.index(b) for b in B])
    return A_max < B_min

def S(A, B):
    ans = 0
    for ordering in all_perms:
        ans += q[ordering] if eval(ordering, A, B) else 0
    return ans

def set_to_string(set):
    res = "{"
    for i, item in enumerate(set):
        res += str(item)
        res += "," if i < len(set)-1 else ""
    res += "}"
    return res

generate_sets()

# create variables
a = {hash(I, i) : model.addVar(name=("a_(%s,%d)" % (set_to_string(I), i))) for I in sets for i in I}
q = {vote : model.addVar(name=("q_%s" % set_to_string(vote))) for vote in all_perms}
assert(len(a) == M*(2**(M-1)-1))
assert(len(q) == factorial(M))

obj = LinExpr()
for I in sets:
    for i in I:
        I_c = U - I
        obj += a[hash(I, i)] * (1 - S({i}, I_c))

# Set objective: maximize x
model.setObjective(obj, GRB.MINIMIZE)

# add linear constraint
one_sum = LinExpr()
for q_var in q.values():
    one_sum += q_var
model.addConstr(one_sum == 1, "∑q=1")

# each q variable has to be non-negative
for i, q_var in enumerate(q.values()):
    model.addConstr(q_var >= 0, "q_%d>=0" % i)

for j in range(1, M+1):
    term = LinExpr()
    for I in sets:
        const = S(I, {j})
        for i in I:
            term += a[hash(I, i)] * const
    model.addConstr(term >= 1, "j=%d" % j)

if __name__ == "__main__":

    # First optimize() call will fail - need to set NonConvex to 2
    """
    try:
        model.optimize()
    except gp.GurobiError:
        print("Optimize failed due to non-convexity")
    """

    #  model.addConstr(a[hash({4}, 4)] == 0, "force singleton 4 to zero")
    # model.addConstr(a[hash({3}, 3)] == 0, "force singleton 3 to zero")
    """permitted = [hash({1}, 1),
                 hash({2}, 2),
                 hash({3}, 3),
                 hash({4}, 4),
                 hash({5}, 5)
                 ]
    for set in sets:
        for i in set:
            if hash(set, i) in permitted:
                continue
            model.addConstr(a[hash(set, i)] == 0, "force %s, %d to zero" % (set, i))
            """
    # Solve bilinear model
    model.Params.NonConvex = 2
    model.Params.Presolve = 1
    # p = model.presolve()
    # print(p.display())
    # print(model.display())
    # model.write("./results/models/%s.mps" % input("Name for original model:\n>>> "))
    # p.write("./results/models/%s.mps" % input("Name for presolved model:\n>>> "))
    model.optimize()

    model.printAttr('x')

    # Constrain 'x' to be integral and solve again
    # x.VType = GRB.INTEGER
    # model.optimize()

    # model.printAttr('x')