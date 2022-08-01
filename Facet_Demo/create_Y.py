import itertools as it
from itertools import chain, combinations
import numpy as np
import pickle
import bz2


unseparables = [1,2]
subsets_unsep = []
for i in range(1,len(unseparables)+1):
    subsets_unsep = subsets_unsep + list(it.combinations(unseparables,i))
subsets_unsep = [set(x) for x in subsets_unsep]


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def satisfies_star(b):
    for x in b:
        for y in subsets_unsep:
            if x.union(y) not in b:
                return False
    return True


num_alts = 5
alts = [x+1 for x in range(num_alts)]
choice_set = []
for i in range(0,num_alts+1):
    choice_set = choice_set + list(it.combinations(alts,i))
choice_set = [set(x) for x in choice_set]
Y_satisfying_star = []
counter = 0
for b in powerset(choice_set):
    if counter%4294967==0:
        print(str(100*counter/4294967296)+'%', end = '\r')
    counter+=1
    if satisfies_star(b):
        Y_satisfying_star.append(b)
print(len(Y_satisfying_star))
ofile = bz2.BZ2File("Y_satisfying_star",'wb')
pickle.dump(Y_satisfying_star, ofile)
ofile.close()
