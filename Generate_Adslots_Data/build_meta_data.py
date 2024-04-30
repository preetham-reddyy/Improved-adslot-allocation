import os
import sys
import random
import json
import pickle
from collections import defaultdict
from matplotlib import pyplot as plt
# from kneed import KneeLocator
plt.switch_backend('agg')
# Path of Data file containing Transactional Data.. I will be using ~/adslot/input/T40I10D100K.dat
DATA_FILE_PATH = sys.argv[1]
AD_SLOTS = map(int,sys.argv[2].split(','))
# MAXOR = str(sys.argv[3])
data_file = open(DATA_FILE_PATH,'r')
view_count=0

dataset_name = ''.join([i for i in DATA_FILE_PATH.split('/')[-1] if i.isalpha()])
# default value if the key doesnt exist in the meta dict
def default_meta_data():
    return {
        'frequency':0,
        'ad_slots':1, #random ad_slot count in this webpage
        'remaining':1,
        'transactions':[]
    }


web_page_meta_dict = defaultdict(default_meta_data)
transaction_no = 1
for transaction in data_file:
    transaction_no += 1
    web_page_list = transaction.split()
    for web_page in web_page_list:
        web_page_meta_dict[web_page]['frequency'] += 1
        web_page_meta_dict[web_page]['transactions'].append(transaction_no)


web_page_freq_sorted = [web_page_number for web_page_number, value in sorted(web_page_meta_dict.items(), key=lambda x:x[1]['frequency'], reverse=True)]
cnt=0
vl=1
# for i in web_page_freq_sorted:
    # cnt+=1
    # if cnt<=33:
    #     vl=5
    # elif cnt<=106:
    #     vl=4
    # elif cnt<=212:
    #     vl=3
    # elif cnt<=392:
    #     vl=2
    # else:
    #     vl=1
    # web_page_meta_dict[i]['ad_slots'] = 1   


data_file.close()


data_file = open(DATA_FILE_PATH,'r')

for transaction in data_file:
    web_page_list = transaction.split()
    for web_page in web_page_list:
        view_count += web_page_meta_dict[web_page]['ad_slots']

data_file.close()
# print(view_count)


y = [value['frequency'] for web_page_number, value in sorted(web_page_meta_dict.items(), key=lambda x:x[1]['frequency'], reverse=True)]
print(web_page_freq_sorted[0])
# print(freqs[0])
x=range(1,len(y)+1,1)
web_page_freq_sorted_file_name  = "web_page_freq_sorted_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,AD_SLOTS)),dataset_name)
web_page_meta_dict_file_name  = "web_page_meta_dict_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,AD_SLOTS)),dataset_name)
# print()

# kn = KneeLocator(range(1,len(y[250:])+1,1), y[250:], curve='convex', direction='decreasing')
# print(kn.knee)
# print("len ikkada")
print("idhoo neeku kaavalsindhi",y[500]," ",y[1000])
print(len(y))
# print(len(y))
#print(y[:600])
#print(y[1000])
for i in range(1,len(y)):
    if y[i]<300:
        print("here is the i"+str(i)+"\n")
        break
# print(y[500])
# print(y[750])
import matplotlib.pyplot as plt
markers_on = [33,106,212,392]
plt.plot(y[:1000],'-gD',markevery=markers_on,mec='grey',mfc='white',color='grey')
plt.ylabel('frequency')
# plt.savefig('books_read.jpeg')
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
# plt.savefig('ksk.eps', format='eps')
plt.savefig('kk.png')
# plt.show()

with open(web_page_freq_sorted_file_name, "wb") as fp:
    pickle.dump(web_page_freq_sorted, fp)

# saving it as json, coz json is luv <3 <3 <3
with open(web_page_meta_dict_file_name, 'w') as fp:
    json.dump(web_page_meta_dict, fp)
print("hey",y[33],y[106],y[212],y[392],y[600],y[-1])
# ivaani debug kosam printing
# print(web_page_freq_sorted[0])
# print(web_page_freq_sorted[-1])
# print(web_page_meta_dict[web_page_freq_sorted[0]])
# print(web_page_meta_dict[web_page_freq_sorted[-1]])
ok = [value['frequency'] for web_page_number, value in sorted(web_page_meta_dict.items(), key=lambda x:x[1]['frequency'], reverse=True)]
