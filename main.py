import numpy as np
import pickle
import string
import math
import dimod
from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

def nb_conflicts(result):
    conflicts = 0
    # lines
    for i in range(n):
        hot = 0
        for j in range(n):
            if result[i*n+j] == 1:
                hot += 1
        if hot > 1:
            conflicts +=1
    #columns
    for j in range(n):
        hot = 0
        for i in range(n):
            if result[i*n+j] == 1:
                hot += 1
        if hot > 1:
            conflicts +=1 
    #descending diagonals
    for k in range(-n+1,n-1):
        hot = 0
        for i in range(n):
            for j in range(n):
                if i-j == k:
                    if result[i*n+j] == 1:
                        hot +=1
        if hot > 1:
            conflicts += 1
    #ascending diagonals
    for k in range(0,2*n-2):
        hot = 0
        for i in range(n):
            for j in range(n):
                if i+j == k:
                    if result[i*n+j] == 1:
                        hot +=1
        if hot > 1:
            conflicts += 1
    return conflicts

def nb_conflicts_list(result):
    conflicts = []
    # lines
    for i in range(n):
        hot = []
        for j in range(n):
            if result[i*n+j] == 1:
                hot.append((i,j))
        if len(hot) > 1:
            conflicts.append(hot)
    #columns
    for j in range(n):
        hot = []
        for i in range(n):
            if result[i*n+j] == 1:
                hot.append((i,j))
        if len(hot) > 1:
            conflicts.append(hot) 
    #descending diagonals
    for k in range(-n+1,n-1):
        hot = []
        for i in range(n):
            for j in range(n):
                if i-j == k:
                    if result[i*n+j] == 1:
                        hot.append((i,j))
        if len(hot) > 1:
            conflicts.append(hot)
    #ascending diagonals
    for k in range(0,2*n-2):
        hot = []
        for i in range(n):
            for j in range(n):
                if i+j == k:
                    if result[i*n+j] == 1:
                        hot.append((i,j))
        if len(hot) > 1:
            conflicts.append(hot)
    return conflicts

n = 8

x = [[dimod.Binary(f'x_{i}_{j}') for j in range(n)] for i in range(n)]

cqm = ConstrainedQuadraticModel()

# only one queen per row
for i in range(n):
    cqm.add_constraint(sum(x[i]) == 1) 

# only one queen per column
for j in range(n):
    cqm.add_constraint(sum(x[i][j] for i in range(n)) == 1) 

# at most one queen on descending diagonal
for k in range(-n+1,n-1):
    cqm.add_constraint(sum(x[i][i-k] for i in range(n) if i-k in range(n)) <= 1)

# at most one queen on ascending diagonal
for k in range(0,2*n-2):
    cqm.add_constraint(sum(x[i][k-i] for i in range(n) if k-i in range(n)) <= 1) 


#print("number of variables: ", cqm.num_quadratic_variables())
#print("variables:", cqm.variables)
#print("constraints: ", cqm.constraints)
#print("objective: ", cqm.objective)

print("calling CQM Solver...")
sampler = LeapHybridCQMSampler()
sampleset = sampler.sample_cqm(cqm, label=str(n)+"-queens")
#print("sampleset:", sampleset)
samples = sampleset.record
energy = samples.energy.min()
print("energy: ", energy)
for i in range(len(samples.energy)):
    result = samples.sample[i]
    #reify the solution as a permutation
    perm = np.zeros((n,), dtype=int)
    for i in range(n):
        for j in range(n):
            if result[(i*n)+j] == 1:
                 perm[i]=j
    print("solution", ":", perm, " with ", nb_conflicts(result), " conflicts")
    #print("solution", ":", perm, " conflicts: ", nb_conflicts_list(result))

