file1 = open('adrepp.txt', 'r')
count=0
st=""
arr=[]
for line in file1:
    count+=1
    if count==1:
        # print(line.strip('\n'))
        temp=line.strip('\n').strip('\n')
        temp=temp.split(" ")
        print((temp))
        if temp[0]=='1':
            arr.append(st)
            st=""
            st+=temp[1]
    elif count==2:
        continue
    else:
        st+=(" "+line.strip('\n'))
        count=0
file1 = open('adreppp.txt', 'w')
file1.write("x y1 y2 y3 y4\n")
for line in arr:
    file1.write(line+"\n")
