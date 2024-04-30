import os
import sys
import random
import json
import pickle
from collections import defaultdict

# Path of Data file containing Transactional Data.. I will be using ~/adslot/input/T40I10D100K.dat
DATA_FILE_PATH = sys.argv[1]
AD_SLOTS = map(int,sys.argv[2].split(',')) # 1,2,3
data_file = open(DATA_FILE_PATH,'r')
dataset_name = ''.join([i for i in DATA_FILE_PATH.split('/')[-1] if i.isalpha()])

# default value if the key doesnt exist in the meta dict
def default_meta_data():
    return {
        'frequency':0,
        'ad_slots':random.choice(AD_SLOTS), #random ad_slot count in this webpage
        'transactions':[]
    }

web_page_meta_dict = defaultdict(default_meta_data)
transaction_no=0
for transaction in data_file:
    transaction_no+=1
    web_page_list = transaction.strip().split(',')
    web_page_list = filter(len, web_page_list)
    for web_page in web_page_list:
        web_page_meta_dict[web_page]['frequency'] += 1
        web_page_meta_dict[web_page]['transactions'].append(transaction_no)

data_file.close()


web_page_freq_sorted_file_name  = "web_page_freq_sorted_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,AD_SLOTS)),dataset_name)
web_page_meta_dict_file_name  = "web_page_meta_dict_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,AD_SLOTS)),dataset_name)
print(web_page_meta_dict_file_name)
web_page_freq_sorted = [(web_page_number, value['frequency']) for web_page_number, value in sorted(web_page_meta_dict.items(), key=lambda x:x[1]['frequency'], reverse=True)]

with open(web_page_freq_sorted_file_name, "wb") as fp:
    pickle.dump(web_page_freq_sorted, fp)

# saving it as json, coz json is luv <3
with open(web_page_meta_dict_file_name, 'w') as fp:
    json.dump(web_page_meta_dict, fp)
