import matplotlib.pyplot as plt
import numpy as np
import pulp as pl

def solveMiningProblem(coefs,qt,v):
    # Problema
    prob = pl.LpProblem("Mineração",pl.LpMaximize)
    
    # Variáveis
    x = [pl.LpVariable(f"x{i}",lowBound=0,upBound=1,cat="Binary") for i in range(1,13)]

    # Função Objetivo
    prob += pl.lpSum(c*y for c,y in zip(coefs,x))
    
    # Restrições
    prob += (pl.lpSum(x) <= qt)
    for i in range(0,4):
        prob += (2*x[i+5] <= x[i] + x[i+1])
    for i in range(5,8):
        prob += (2*x[i+4] <= x[i] + x[i+1])
        
    # Item B
    prob += (pl.lpSum(w*y for w,y in zip(v,x)) <= 10000)
    
    # Item C
    a = [pl.LpVariable(f"a{i}",lowBound=0,upBound=1,cat="Binary") for i in range(1,6)]
    b = [pl.LpVariable(f"b{i}",lowBound=0,upBound=1,cat="Binary") for i in range(1,6)]
    c = [pl.LpVariable(f"c{i}",lowBound=0,upBound=1,cat="Binary") for i in range(1,6)]
    d = [pl.LpVariable(f"d{i}",lowBound=0,upBound=1,cat="Binary") for i in range(1,10)]
    prob += (pl.lpSum(a) <= 1)
    prob += (pl.lpSum(b) <= 1)
    prob += (pl.lpSum(c) <= 1)
    prob += (pl.lpSum(d) <= 1)
    for i in range(5):
        prob += ((a[i] + b[i] + c[i] + d[i]) <= x[i])
    for i in range(5,9):
        prob += (d[i] <= x[i])
    prob += ((pl.lpSum([coefs[i]*(a[i]+b[i]+c[i]+d[i]) for i in range(5)]))+(coefs[5]*d[5]+coefs[6]*d[6]+coefs[7]*d[7]+coefs[8]*d[8]) >= 20)
    
    # Solução do Solver
    prob.solve(pl.PULP_CBC_CMD(msg=False))
    print(f"a: {[int(aa.varValue) for aa in a]}")
    print(f"b: {[int(bb.varValue) for bb in b]}")
    print(f"c: {[int(cc.varValue) for cc in c]}")
    print(f"d: {[int(dd.varValue) for dd in d]}")
    print(f"{[int(k.varValue) for k in x]} -> {int(prob.objective.value())}")

#solveMiningProblem(coefs=[1, 8, 3, 6, 7, 5, 6, 9, 5, 12, 17, 14],qt=7,v=[385, 1135, 6946, 1393, 355, 599, 963, 1646, 2444, 1992, 1935, 2445])

def examplouw():
    prob = pl.LpProblem("V", pl.LpMaximize)

    x1 = pl.LpVariable("x1", lowBound=0)
    x2 = pl.LpVariable("x2", lowBound=0)

    prob += (2*x1 + x2, "Z")
    prob += (12*x1 + 3*x2 <= 6, "R1")
    prob += (-3*x1 + x2 <= 7, "R2")
    prob += (x2 <= 10, "R3")

    prob.solve(pl.PULP_CBC_CMD(msg=False))

    for name, constraint in prob.constraints.items():
        print(f"{name} Folga = ", constraint.slack)
        
    for name, constraint in prob.constraints.items():
        print(f"{name} Preço Sombra = ", constraint.pi)

import gurobipy as gp

def gurobi():
    model = gp.Model("ToyToyToy")
    model.Params.LogToConsole = 0
    
    x1 = model.addVar(lb=0, name="x1")
    x2 = model.addVar(lb=0, name="x2")
    
    model.setObjective(2*x1 + x2, gp.GRB.MAXIMIZE)
    
    constr1 = model.addConstr(12*x1 + 3*x2 <= 6, "r1")
    constr2 = model.addConstr(-3*x1 + x2 <= 7, "r2")
    constr3 = model.addConstr(x2 <= 10, "r3")

    model.optimize()
    
    if model.status == gp.GRB.OPTIMAL:
        print("Intervalos para coeficientes da função objetivo")
        print("Para x1:")
        print(f"  Coeficiente atual: {x1.obj}")
        print(f"  Intervalo: [{x1.SAObjLow}, {x1.SAObjUp}]")
        print("Para x2:")
        print(f"  Coeficiente atual: {x2.obj}")
        print(f"  Intervalo: [{x2.SAObjLow}, {x2.SAObjUp}]")
    
        print("Intervalos de Lado Direito")
        print("Para restrição 1 (12x1 + 3x2 ≤ 6):")
        print(f"  RHS atual: {constr1.rhs}")
        print(f"  Limite inferior: {constr1.SARHSLow}")
        print(f"  Limite superior: {constr1.SARHSUp}")
        print("Para restrição 2 (-3x1 + x2 ≤ 7):")
        print(f"  RHS atual: {constr2.rhs}")
        print(f"  Limite inferior: {constr2.SARHSLow}")
        print(f"  Limite superior: {constr2.SARHSUp}")
        print("Para restrição 3 (x2 ≤ 10):")
        print(f"  RHS atual: {constr3.rhs}")
        print(f"  Limite inferior: {constr3.SARHSLow}")
        print(f"  Limite superior: {constr3.SARHSUp}")
        
def conway(n):
    p = pl.LpProblem("Conway",pl.LpMaximize)
    
    x = [[pl.LpVariable(f"X_{i}_{j}",cat="Binary",lowBound=0,upBound=1) for j in range(1,n+1)] for i in range(1,n+1)]
    y = [[pl.LpVariable(f"Y_{i}_{j}",cat="Binary",lowBound=0,upBound=1) for j in range(1,n+1)] for i in range(1,n+1)]
    
    def viz(i,j):
        v = []
        for l in range(max(i-1,0),min(i+2,n)):
            for c in range(max(j-1,0),min(j+2,n)):
                if(l != i or c != j): v.append(x[l][c])
        return v
    
    p += pl.lpSum(x)
    for i in range(n):
        for j in range(n):
            p += (2 <= pl.lpSum(viz(i,j)) + 10*(1-x[i][j]))
            p += (pl.lpSum(viz(i,j)) <= 3 + 10*(1-x[i][j]))
            p += (pl.lpSum(viz(i,j)) <= 2 + 10*(y[i][j]))
            p += (pl.lpSum(viz(i,j)) >= 4 - 10*(1-y[i][j]))
            
    p.solve(pl.PULP_CBC_CMD(msg=False))
    
    print(f'Densidade Máxima: {(p.objective.value()/(n*n)):.2f}')
    
    print(f'X: ')
    for i in range(n):
        for j in range(n):
            print(int(x[i][j].varValue),end=" ")
        print()
conway(7)