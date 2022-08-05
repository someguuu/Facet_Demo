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

# example_Y = [{1,2,3}]
# example_Y = [{1,2}, {1,2,3}, {1,2,3,4}]
# example_Y = [{1,3}, {1,2,3}]
# example_Y = [{1,2}, {1,2,3}, {1,2,3,5}]
example_Y = [{1,2,3}, {1,2,3,4}]
redundant_Y = check_redundancy(points, Y_satisfying_star, example_Y, 100)
for Y in redundant_Y:
    print(reduce_to_generator(list(Y)))
print(len(redundant_Y))


# example_Y = [set()]
# not_satisfies_conditions = 0
# for point in points:
#     if calculate_feasibility_condition(point, example_Y) < -10e-15:
#         not_satisfies_conditions += 1
# print("Checking non-random utility (the number should be close to 1 if the condition is sufficient): {}".format((not_satisfies_conditions)/(len(points))))
# print(not_satisfies_conditions)
