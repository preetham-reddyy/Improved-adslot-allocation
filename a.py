from bisect import bisect_left, bisect_right
import numpy as np
import sys
import os



with open("freq1.txt") as f:
    content = f.readlines()
print("Done reading file")
content = [x.strip() for x in content]
freq_arr = []
freq_dict = {}
index_dict = {}
count = 0
for i in content:
    k = i.split(" ")
    freq_arr.append([k[0], int(k[1])])
    freq_dict[k[0]] = int(k[1])
    index_dict[k[0]] = count
    count += 1
with open("real.txt") as f:
    content = f.readlines()
print("Done reading file b.txt")
content = [x.strip() for x in content]
data = content

with open("realcp_0005_0.txt") as f:
    content = f.readlines()
print("Done reading file blah")

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))
def getUniqueness(string, lastPatternItem):
    # print(type(string),string)
    q = int(string[1:int(string[0])+1])
    r = int(string[int(string[0])+2:])
    ovr = r*100000.0/freq_dict[str(lastPatternItem)]
    return abs(ovr-q), q


# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
patterns = []
for i in content:
    # print(i)
    patternString = i.split(" ")[0]
    string = i.split(" ")[1]
    patternItems = list(map(str, patternString.split("|")))
    # print(q,r,l)
    # exit()
    patternFreq = 0
    for item in patternItems:
        patternFreq = patternFreq + freq_dict[str(item)]
    uniqueness, cs = getUniqueness(string, patternItems[-1])
    # print(patternItems)
    # print(string)
    # print(patternItems[-1])
    # print(uniqueness)
    # exit()

    patterns.append({
        'pattern': patternItems,
        'pattern_freq': patternFreq,
        'uniqueness': uniqueness,
        'cs': cs})
print("Done generating patterns", len(patterns), patterns[0])
patterns.sort(key=lambda x: (x['pattern_freq'], x['uniqueness']), reverse=True)
print("Done sorting patterns", len(patterns))
# count=0
# sum=0
# l=np.array
# for i in patterns:
#     count=count+1
#     sum=sum+i[1]
#     l=np.append(l,np.array(i[1]))
# sum=sum/count
# print(p[1])
# print(np.var(l))
bitArr = {}
for i in range(len(data)):
    patt = data[i].split()
    for j in range(len(patt)):
        if patt[j] not in bitArr:
            bitArr[patt[j]] = set()  # np.full((100000), False, dtype=np.bool)
        # if i not in bitArr[patt[j]]:
        bitArr[patt[j]].add(i)
print("Done generating bitarr")
# bitArrPattern = []
key = 64
overlap = []
# patterns[key]['pattern']
p = [56,320,381]
keyed_pattern = list(map(str, p))
# print(patterns[key])

key_orred = set()
for item in keyed_pattern:
    key_orred = key_orred.union(bitArr[item])

for patt in patterns:
    pattList = patt['pattern']
    orred = set()  # np.full((100000,1), False, dtype=np.bool)
    for item in pattList:
        orred = orred.union(bitArr[item])  # np.logical_or(orred,bitArr[item])
    overlap.append(key_orred.intersection(orred).__len__())
    # bitArrPattern.append(orred)

# print("Done generating bitarrpattern")
# overlap = []
# for arr in bitArrPattern:
    # overlap.append(np.sum(np.logical_and(bitArrPattern[key],arr)))
    # overlap.append(arr.intersection(bitArrPattern[key]).__len__())
print("Done calc overlap")
with open("file1.txt", "w") as f:
    for i in range(len(overlap)):
        if(len(intersection(p, patterns[i]['pattern'])) == 0):
            f.write(str(overlap[i]) + "//"+str(patterns[i]['cs'])+"\t" + str(
                overlap[i]*100.0/patterns[i]['cs'])+"%"+"\t"+",".join(patterns[i]['pattern'])+"\n")
print("Done")


# def BinarySearch(a, x):
#     i = bisect_right(a, x)
#     if i:
#         if i >0  and a[i-1] == x:
#             return i -1
#         return i
#     else:
#         return -1


# pattern_freq = [a['pattern_freq'] for a in patterns]
# x = int(30)
# res = BinarySearch(pattern_freq, x)
# if res == -1:
#     print("No value smaller than ", x)
# else:
#     print(a[res],res)
#     # print("Largest value smaller than ", x, " is at index ", res)

# # def assignPattern(patterns,)
# end=res
# start=res
# cur=res

# while pattern_freq[cur-1] == pattern_freq[res]:
#     cur-=1