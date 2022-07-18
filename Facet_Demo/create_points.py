import itertools as it
import numpy as np
import pickle
import bz2

def rhopi(pi, d, x):
    if x not in d:
        return 0
    for i in d:
        if pi.index(i) > pi.index(x):
            return 0
    return 1

num_alts = 5
alts = [x+1 for x in range(num_alts)]
choice_set = []
for i in range(1,num_alts+1):# 3 is the mimial size
    choice_set = choice_set + list(it.combinations(alts,i))
print(choice_set[0])
rhos = []
for i in range(1000):
    if i%100000 == 0:
        print(str(i/100000)+"%")
    rho = {}
    for issue in choice_set:
        rho_d = {}
        weights = np.random.rand(len(issue))
        weights = weights/np.sum(weights)
        for i in range(len(issue)):
            rho_d[issue[i]] = weights[i]
        rho[issue] = rho_d
    rhos.append(rho)
ofile = bz2.BZ2File("points",'wb')
pickle.dump(rhos, ofile)
ofile.close()