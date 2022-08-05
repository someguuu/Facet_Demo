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
for i in range(1,num_alts+1):
    choice_set = choice_set + list(it.combinations(alts,i))
print(choice_set[0])
rhos = []
for i in range(100000):
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

# The following makes sure that generated choice functions satisfy r(D3, D4) >= 0
# for i in range(len(rhos)):
# 	# i = 0
# 	for x in alts:
# 		# x = alts[0]
# 		issue = [elem for elem in alts if elem != x]
# 		weights = np.random.rand(len(issue))
# 		weights = weights/np.sum(weights)
# 		for y, weight in zip(issue, weights):
# 			# y = issue[0]
# 			rhos[i][tuple(issue)][y] = rhos[i][tuple(alts)][y] + rhos[i][tuple(alts)][x] * weight

ofile = bz2.BZ2File("points",'wb')
pickle.dump(rhos, ofile)
ofile.close()