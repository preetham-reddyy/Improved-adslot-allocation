import sys
import time
import cmine

# GIVE INPUT IN THE FORM
# python3 run.py <adressof_inputdatafile>


def binarySearch(arr, l, r, x):

    # Check base case
    if r >= l:

        mid = l + (r - l)/2

        # If element is present at the middle itself
        if arr[mid][4] == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid][4] > x:
            return binarySearch(arr, l, mid-1, x)

        # Else the element can only be present in right subarray
        else:
            return binarySearch(arr, mid+1, r, x)

    else:
        # Element is not present in the array
        return -1


t1 = time.clock()
# minRF = float(sys.argv[1])
# minCS = float(sys.argv[2])
# maxOR = float(sys.argv[3])
inpfile = sys.argv[1]
obj = cmine.cmine(inpfile)
candidate_patterns = obj.expand()

print("total candidates", candidate_patterns)
ranked_pttrns = sorted(obj.cvg_pttrn, key=lambda a: (-a[4], -a[3]))
final_pttrns = ranked_pttrns
seti = []
print("initial sorted \n")
for i in ranked_pttrns:
    print(str(i)+"\n")
rem = []
for i in ranked_pttrns:
    # print(str(i)+"\n")
    buffer = []
    flag = 0
    for j in i[0]:
        if j not in seti:
            buffer.append(j)

        else:
            rem = rem+[i]
            flag = 1
            break

    if flag == 0:
        seti = seti + buffer


for i in rem:
    ranked_pttrns.remove(i)

# demand_set = []
# dem_set = demand_set
# alloted = [None] * len(demand_set)

# for i in demand_set:
#     index = binarySearch(ranked_pttrns, 0, len(ranked_pttrns)-1, i)
#     if abs(ranked_pttrns[i])


print("\n final sorted \n")
for i in ranked_pttrns:
    print(str(i)+"\n")

with open('final_output.txt', 'w') as f:
    for ele in ranked_pttrns:
        f.write(str(ele)+'\n')

t2 = time.clock()
print("process done", str(t2-t1))
