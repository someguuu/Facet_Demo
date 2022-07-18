import itertools as it
import numpy as np
import pickle
import bz2

num_alts = 5
alts = [x+1 for x in range(num_alts)]
choice_set = []
for i in range(1,num_alts+1):# 3 is the mimial size
    choice_set = choice_set + list(it.combinations(alts,i))
choice_set = [list(x) for x in choice_set]

def rho(point, d, x):
    return point[tuple(d)][x]

def weight_points(coefs, vertices):
    point = {}
    for d in vertices[0].keys():
        point[d] = dict(vertices[0][d])
        for x in vertices[0][d].keys():
            temp = 0
            count = 0
            for i in range(len(vertices)):
                temp += vertices[i][d][x]*coefs[i]
                count += 1
            point[d][x] = temp
    return point

def is_subset(superset, subset):
    return all(item in superset for item in subset)

def partial_BS(p, d, x): #partial_block_marchack
    out = 0
    notd = [x for x in alts if x not in d]
    enotd = []
    for i in range(1,len(notd)+1):# 3 is the mimial size
        enotd = enotd+list(it.combinations(notd,i))
    enotd = [list(x) for x in enotd]
    for e in [sorted(d+x) for x in enotd if len(x)+len(d) != 3]:
        summand = rho(p,e,x)*((-1)**(len(e)-len(d)))
        out += summand
    return out

def BS(p, d, x):
    out = 0
    notd = [x for x in alts if x not in d]
    enotd = []
    for i in range(1,len(notd)+1):# 3 is the mimial size
        enotd = enotd+list(it.combinations(notd,i))
    enotd = [list(x) for x in enotd]
    for e in [sorted(d+x) for x in enotd if len(x)+len(d) != 3]:
        summand = rho(p,e,x)*((-1)**(len(e)-len(d)))
        out += summand
    return out

def subsets_of_size(n):
    return [list(x) for x in list(it.combinations(alts, n))]

def go_up(d, x):
    temp = d[:]
    temp.append(x)
    temp.sort()
    return temp

def go_down(d,x):
    temp = d[:]
    temp.remove(x)
    return temp

def all_conditions(conditions, point):
    for f in conditions:
        if not f(point):
            return False
    return True

def inflow_outflow(point):
    for d3 in subsets_of_size(3): #d3 is a set of size 3
        outflow = 0     
        for x in [x for x in alts if x not in d3]:
            outflow += partial_BS(point, go_up(d3,x), x) #    flow from d3 uion x to x
        inflow = 0
        for x in d3:
            inflow += partial_BS(point, d3, x)    #flow into d3
        if outflow-inflow < 0:
            return False
    return True

def lower_upper_equality(point):
    for d1 in subsets_of_size(1):
        left = partial_BS(point, d1, d1[0])
        right = 0
        for d2 in [d2 for d2 in subsets_of_size(2) if is_subset(d2,d1)]:
            left += partial_BS(point, d2, d1[0])
        for d3 in [d3 for d3 in subsets_of_size(3) if is_subset(d3,d1)]:
            left += partial_BS(point, d3, d1[0])
            for x in [x for x in alts if x not in d3]:
                right += partial_BS(point, go_up(d3, x), x)
        #print(left,right)
        if abs(left-right) > 10e-15:
            return False
    return True

def upper_bounds_ineq(point):
    for d2 in subsets_of_size(2):
        for x in d2:
            if partial_BS(point, d2, x) < 0:
                return False
    return True

def lower_bounds_ineq(point):
    for d3 in subsets_of_size(3):
        out = 1
        for x in d3:
            out += partial_BS(point, d3, x)
        if out < 0:
            return False
    return True

def upper_lower_equality(point):
    for d2 in subsets_of_size(2):
        left = 0
        right = 0
        for x in d2:
            left += partial_BS(point, d2, x)
        for d3 in [d3 for d3 in subsets_of_size(3) if is_subset(d3,d2)]:
            for x in d2:
                left += partial_BS(point, d3, x)
            for x in [x for x in alts if x not in d3]:
                right += partial_BS(point, go_up(d3, x), x)
        if abs(left-right) > 10e-15:
            return False
    return True

def BS_size_3_all_nonneg(point):
    for d4 in subsets_of_size(4):
        for x in d4:
            if partial_BS(point, d4, x) < 0:
                return False
    return True

def satisfies_all_BS(point):
    for d in choice_set:
     for x in d:
         if BS(point, d, x) < 0:
                return False
    return True

#Tests conditions for case where information is missing

def try_conditions(points, conditions):
    counterexamples = 0
    satisfiesbs = 0
    negativek = 0
    for point in points:
        outbs = all_conditions(conditions, point) # whehter a sample of non-random utilitys satises all conditions or not
        if satisfies_all_BS(point):
            satisfiesbs += 1
        if not outbs:
            negativek +=1
        # else:
        #     print(weight_points(affine, vertices))
    return {"inside" : counterexamples, "outside": negativek, "satisfiesbs": satisfiesbs}

conditions = [inflow_outflow, upper_bounds_ineq, lower_bounds_ineq, upper_lower_equality, lower_upper_equality, BS_size_3_all_nonneg]
#conditions = [upper_lower_equality]
#conditions = [inflow_outflow]
#print(try_conditions(trials, conditions))
#result = try_conditions(trials, [inflow_outflow, upper_bounds_ineq, lower_bounds_ineq])
# result = try_conditions(trials, [lower_upper_equality, upper_lower_equality])
ifile = bz2.BZ2File("points",'rb')
points = pickle.load(ifile)
ifile.close()
result = try_conditions(points, conditions)
#print("Checking random utility model (the number should be close to 0 if the condition is necessary): {}".format(result["inside"]/trials))
print("Checking non-random utility (the number should be close to 1 if the condition is sufficient): {}".format((result["outside"]-result["satisfiesbs"])/(len(points)-result["satisfiesbs"])))
print(result)