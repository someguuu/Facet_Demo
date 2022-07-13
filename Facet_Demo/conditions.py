import itertools as it
import numpy as np
import pickle

numalts = 5
alts = [x+1 for x in range(numalts)]
choiceset = []
for i in range(1,numalts+1):# 3 is the mimial size
  choiceset = choiceset + list(it.combinations(alts,i))
choiceset = [list(x) for x in choiceset]

def rho(point, d, x):
  return point[choiceset.index(d)][d.index(x)]

def weightpoints(coefs, vertices):
  point = {}
  for key in vertices[0].keys():
    temp = 0
    count = 0
    for i in range(len(vertices)):
      temp += vertices[i][key]*coefs[i]
      count += 1
    point[key] = temp
  return point

def issubset(superset, subset):
  return all(item in superset for item in subset)

def k(p, d, x): #partial_block_marchack
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

def kfull(p, d, x):
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

def d(n):
  return [list(x) for x in list(it.combinations(alts, n))]

def goUp(d, x):
  temp = d[:]
  temp.append(x)
  temp.sort()
  return temp

def goDown(d,x):
  temp = d[:]
  temp.remove(x)
  return temp

def bs(coefs):
 out = []
 point = weightpoints(coefs, vertices)
 for d in choiceset:
   for x in d:
     out.append(kfull(point,d,x))
 return out

def allconditions(conditions, point):
  for f in conditions:
    if not f(point):
      return False
  return True

def inout(point):
  for d3 in d(3): #d3 is a set of size 3
    outflow = 0   
    for x in [x for x in alts if x not in d3]:
      outflow += k(point, goUp(d3,x), x) #  flow from d3 uion x to x
    inflow = 0
    for x in d3:
      inflow += k(point, d3, x)  #flow into d3
    if outflow-inflow < 0:
      return False
  return True

def lowerupperequality(point):
  for d1 in d(1):
    left = k(point, d1, d1[0])
    right = 0
    for d2 in [d2 for d2 in d(2) if issubset(d2,d1)]:
      left += k(point, d2, d1[0])
    for d3 in [d3 for d3 in d(3) if issubset(d3,d1)]:
      left += k(point, d3, d1[0])
      for x in [x for x in alts if x not in d3]:
        right += k(point, goUp(d3, x), x)
    #print(left,right)
    if abs(left-right) > 10e-15:
      return False
  return True

def upperboundsineq(point):
  for d2 in d(2):
    for x in d2:
      if k(point, d2, x) < 0:
        return False
  return True

def lowerboundsineq(point):
  for d3 in d(3):
    out = 1
    for x in d3:
      out += k(point, d3, x)
    if out < 0:
      return False
  return True

def upperlowerequality(point):
  for d2 in d(2):
    left = 0
    right = 0
    for x in d2:
      left += k(point, d2, x)
    for d3 in [d3 for d3 in d(3) if issubset(d3,d2)]:
      for x in d2:
        left += k(point, d3, x)
      for x in [x for x in alts if x not in d3]:
        right += k(point, goUp(d3, x), x)
    if abs(left-right) > 10e-15:
      return False
  return True

def nonnegineq(point):
  for d4 in d(4):
    for x in d4:
      if k(point, d4, x) < 0:
        return False
  return True

def satisfiesallbs(point):
  for d in choiceset:
   for x in d:
     if kfull(point, d, x) < 0:
       return False
  return True

#Tests conditions for case where information is missing

def tryconditions(points, conditions):
  counterexamples = 0
  satisfiesbs = 0
  negativek = 0
  for point in points:
    outbs = allconditions(conditions, point) # whehter a sample of non-random utilitys satises all conditions or not
    if satisfiesallbs(point):
      satisfiesbs += 1
    if not outbs:
      negativek +=1
    # else:
    #   print(weightpoints(affine, vertices))
  return {"inside" : counterexamples, "outside": negativek, "satisfiesbs": satisfiesbs}

conditions = [inout, upperboundsineq, lowerboundsineq, upperlowerequality, lowerupperequality]
conditions = [nonnegineq]
#conditions = [inout]
#print(tryconditions(trials, conditions))
#result = tryconditions(trials, [inout, upperboundsineq, lowerboundsineq])
# result = tryconditions(trials, [lowerupperequality, upperlowerequality])
with open("points", 'rb') as f:
    points = pickle.load( f)
result = tryconditions(points, conditions)
#print("Checking random utility model (the number should be close to 0 if the condition is necessary): {}".format(result["inside"]/trials))
print("Checking non-random utility (the number should be close to 1 if the condition is sufficient): {}".format((result["outside"]-result["satisfiesbs"])/(len(points)-result["satisfiesbs"])))
print(result)