# import numpy as geek 
   
# # 1D Array 
# array = geek.random.normal(40650.71744898646, 40000, 20) 
# print(array)


import numpy

from random import gauss
n = 30
values = []
frequencies = {}
while len(values) < n:
    value = gauss(40650.71744898646, 13000)
    # if 21254 < value < 65211:
    if 0 < value < 65211:
        frequencies[int(value)] = int(frequencies.get(int(value), 0)) + 1
        values.append(int(value))
print(len(values),values)
print(min(values),max(values))