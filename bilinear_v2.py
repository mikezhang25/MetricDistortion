from math import factorial
import itertools
import gurobipy as gp
from gurobipy import GRB, LinExpr

# CONSTANTS
M = 3
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

def not_S(A, B):
    """ Proportion of votes where there A is *not* completely above B"""
    total_q = 0
    for ordering in all_perms:
        total_q += q[ordering]
    return total_q - S(A, B)

def S(A, B):
    """ Proportion of votes where A is completely above B """
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
        obj += a[hash(I, i)] * (not_S({i}, I_c)) # here, we want to set obj to not S

# Set objective: maximize x
model.setObjective(obj, GRB.MINIMIZE)

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

    # Solve bilinear model
    model.Params.NonConvex = 2
    model.Params.Presolve = 1
    model.presolve()
    model.optimize()

    model.printAttr('x')

    # Constrain 'x' to be integral and solve again
    # x.VType = GRB.INTEGER
    # model.optimize()

    # model.printAttr('x')