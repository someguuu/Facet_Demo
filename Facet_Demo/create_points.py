import itertools as it
import numpy as np
import pickle

def rhopi(pi, d, x):
  if x not in d:
    return 0
  for i in d:
    if pi.index(i) > pi.index(x):
      return 0
  return 1

numalts = 5
alts = [x+1 for x in range(numalts)]
choiceset = []
for i in range(1,numalts+1):# 3 is the mimial size
  choiceset = choiceset + list(it.combinations(alts,i))
choiceset = [list(x) for x in choiceset]
rhos = []
for i in range(1000000):
    if i%100000 == 0:
      print(str(i/100000)+"%")
    rho = []
    for issue in choiceset:
        weights = np.random.rand(len(issue))
        weights = weights/np.sum(weights)
        rho.append(weights)
    rhos.append(rho)
with open("points", 'wb') as f:
    pickle.dump(rhos, f)