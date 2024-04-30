import os
import sys
import pickle
import json
import re
import bisect
import itertools

lines = []
inp=sys.argv[1]
otp=sys.argv[2]
with open(inp) as f:
    lines = f.readlines()

file1 = open(otp, "a")
S = set()
for line in lines:
    line=line.strip().split(" ")
    for word in line:
        if word not in S and word != "":
            S.add(word)
    outstr = ""
    for key in S:
        outstr += str(key)
        outstr += " "
    outstr=outstr[:-1]
    outstr += "\n"
    file1.write(outstr)

# file1 = open("output.txt", "r")
# print("Output of Readlines after appending")
# print(file1.read())
# print()
file1.close()
