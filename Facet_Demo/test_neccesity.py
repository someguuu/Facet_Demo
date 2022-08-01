import itertools as it
import numpy as np
import pickle
import bz2
from conditions import *


ifile = bz2.BZ2File("Y_satisfying_star",'rb')
Y_satisfying_star = pickle.load(ifile)
ifile.close()

print("loaded")
numalts = 5
alts = [x+1 for x in range(numalts)]
choiceset = []
for i in range(1,numalts+1):
  choiceset = choiceset + list(it.combinations(alts,i))
orders = list(it.permutations(alts))
choiceset = [list(x) for x in choiceset]
orders = [list(x) for x in orders]


vertices = []
for pi in orders:
  vertex={}
  for d in choiceset:
    rho_d = {}
    for x in alts:
      rho_d[x] = rhopi(pi, d, x)
    vertex[tuple(d)] = rho_d
  vertices.append(vertex)

trials = 1
not_satisfies_conditions = 0
for i in range(trials):
    print(i)
    convex = np.random.rand(len(vertices))
    convex = convex/(np.sum(convex)) #weights that generate random utility 
    point = weight_points(convex, vertices)
    if not satisfies_feasibility_condtitions(point, Y_satisfying_star):
        not_satisfies_conditions += 1
print("Checking random utility model (the number should be close to 0 if the condition is necessary): {}".format(not_satisfies_conditions/trials))
print(not_satisfies_conditions)