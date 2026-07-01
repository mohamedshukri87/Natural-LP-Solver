#
# 
# I'm a farmer with 100 acres. Wheat earns £200/acre, corn earns £300/acre. 
# I have a £10,000 budget — wheat costs £80/acre to plant, corn costs £150/acre. 
# How do I maximise profit?


import pulp
from pulp import LpStatus
from pulp import LpVariable

def solve(problem):
    variables = []

    # FIX MAXIMISE OR MINIMISE
    model = pulp.LpProblem("MaximiseProfit", pulp.LpMaximize)

    variables = [LpVariable(name, lowBound = 0) for name in problem['variables']]

    model += pulp.lpSum(
            variables[i] * problem["objective_coefficients"].get(problem["variables"][i], 0)
            for i in range(len(variables))
    )
    for c in problem['constraints']:
        model += pulp.lpSum(
            variables[i] * c["coefficients"].get(problem["variables"][i], 0)
            for i in range(len(variables)) 
        ) <= c["rhs"]

    model.solve()



    return model

