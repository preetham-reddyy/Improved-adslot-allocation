import os
import sys
import random
data_set = sys.argv[1]
data_file = open(data_set,'r')
file1 = open('clean_bmspos.txt', 'w') 
Lines = data_file.readlines()
L=[] 
for line in Lines:
    if line.split(' ')[0] == "3":
        L.append(line)
file1.writelines(L) 
file1.close() 

for transaction in data_file:
    web_page_list = transaction.split()
    for web_page in web_page_list:
        web_page_meta_dict[web_page]['frequency'] += 1

data_file.close()
