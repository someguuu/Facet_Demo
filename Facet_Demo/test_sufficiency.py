import itertools as it
import numpy as np
import pickle
import bz2
from conditions import *

ifile = bz2.BZ2File("points",'rb')
points = pickle.load(ifile)
ifile.close()

ifile = bz2.BZ2File("Y_satisfying_star",'rb')
Y_satisfying_star = pickle.load(ifile)
ifile.close()

print("loaded")

not_satisfies_conditions = 0
satisfies_BS = 0
for point in points:
    if not satisfies_feasibility_condtitions(point, Y_satisfying_star):
        not_satisfies_conditions += 1
    if satisfies_all_BS(point):
        satisfies_BS += 1
print("Checking non-random utility (the number should be close to 1 if the condition is sufficient): {}".format((not_satisfies_conditions-satisfies_BS)/(len(points)-satisfies_BS)))
print(not_satisfies_conditions)