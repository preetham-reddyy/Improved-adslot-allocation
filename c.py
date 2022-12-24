import sys

arr=[]
count=0
f=open(sys.argv[1],'r')
for row in f:
        count+=1
        row=row.rstrip('\n')
        row1=row
        if count<839:
                row=row.strip(' ')
                row=row.split(' ')
#       print row
                row1=row[0]+str(len(row[1])-1)+row[1]
                row1=row1.split(']')[0]
                arr.append(row1+"10]")
        else:
                arr.append(row1)
f=open("hey.txt",'w')

for row in arr:
        f.write(row+'\n')
f.close()
