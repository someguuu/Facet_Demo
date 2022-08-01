import itertools as it
import numpy as np
import pickle
import bz2
from conditions import *

def rhopi(pi, d, x):
  if x not in d:
    return 0
  for i in d:
    if pi.index(i) > pi.index(x):
      return 0
  return 1


def partial_BS_star(p, d, a): #partial block marchack without unseparable information
    out = 0
    notd = [x for x in alts if x not in d]
    enotd = []
    for i in range(0,len(notd)+1):
        enotd = enotd+list(it.combinations(notd,i))
    enotd = [list(x) for x in enotd]
    for e in [sorted(d+x) for x in enotd if a not in unseparables or not all(item in d or item in x for item in unseparables)]:
        summand = rho(p,e,a)*((-1)**(len(e)-len(d)))
        out += summand
    return out

def satisfies_feasibility_condtitions(point):
    for Y in Y_satisfying_star:
        if alts in Y and set() not in Y:
            sum = -1
        elif alts not in Y and set() in Y:
            sum = 1
        else:
            sum = 0
        for D in Y:
            for x in alts:
                if x not in D and x not in unseparables and D.union({x}) not in Y:
                    sum += partial_BS_star(point, sorted(list(D.union({x}))), x)
            for x in D:
                if D.difference({x}) not in Y:
                    sum -= partial_BS_star(point, sorted(list(D)), x)
        if sum < 0:
            return False
    return True


ifile = bz2.BZ2File("Y_satisfying_star",'rb')
Y_satisfying_star = pickle.load(ifile)
ifile.close()

print("loaded")
unseparables = [1,2]
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

trials = 10
not_satisfies_conditions = 0
for i in range(trials):
    affine = np.random.normal(size = len(vertices)) 
    affine = affine/np.sum(affine)
    point = weight_points(affine, vertices)
    if not satisfies_feasibility_condtitions(point):
        not_satisfies_conditions += 1
print("Checking random utility model (the number should be close to 0 if the condition is necessary): {}".format(not_satisfies_conditions/trials))
print(not_satisfies_conditions)