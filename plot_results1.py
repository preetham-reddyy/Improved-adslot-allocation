#!/usr/bin/env python

import os
import sys
import json
import random
import numpy as np
from matplotlib import pyplot as plt
import time

current_milli_time = lambda: int(round(time.time() * 1000))
# for matplotlib to work
plt.switch_backend('agg')

# number of advertisers
advertiser_lengths = range(10,100,10)

# cmine tharvatha vachina file
# if len(sys.argv) !=2:
#     print("Sarriga arguments ichi dobichuko")
#     sys.exit(1)
# else:
    # PATTERNS_FILE_PATH = "../test1/dataset_bms_pos.txt_0.065_0.0_0.6_output.txt"
PATTERNS_FILE_PATH = sys.argv[1] #
# kindha advertisers data generate cheyadanki
ar1= 50000 #int(sys.argv[2])
mean_list = [ar1]*len(advertiser_lengths)

DATA_FILE_PATH = sys.argv[2]
# AD_SLOTS = map(int,sys.argv[3].split(','))
dataset_name = ''.join([i for i in DATA_FILE_PATH.split('/')[-1] if i.isalpha()])

# build_meta_data.py nunchi vachina two files
DELTA=[2] #, 4, 6, 8, 10]

web_page_freq  = "/home/preetham_sathineni/adslot/web_page_freq_sorted_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[1])),dataset_name)
web_page_meta  = "/home/preetham_sathineni/adslot/web_page_meta_dict_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[1])),dataset_name)

# idhi mana transactional data (dataset)
transactional_data = DATA_FILE_PATH

new_method =[]
oneslot_method =[]
VFS_method=[]

def to_int_str(value):
    return str(int(value))

def get_me_a_tmp_file():
    random_num = current_milli_time()
    tmp_file = "/tmp/{0}.txt".format(str(random_num))
    os.system("touch {}".format(tmp_file))
    return tmp_file

k=101
for j in DELTA:
    for i in range(len(advertiser_lengths)):
        web_page_freq_sorted  = "/home/preetham_sathineni/adslot/web_page_freq_sorted_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[k])),dataset_name)
        web_page_meta_dict  = "/home/preetham_sathineni/adslot/web_page_meta_dict_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[k])),dataset_name)
        # This is random distribution between min and max values
        # adv_str = ','.join(map(str,[random.randint(100000,250000) for i in range(advertiser_length)]))
        # this is uniform distribution for given mean and variance
        advertiser_length = advertiser_lengths[i]
        #ee block to generate advertisers data
        mean = mean_list[i]
        variance = 500
        samples = advertiser_length
        print("ALLOCATING WITH OUR NEW METHOD: "+str(advertiser_length))
        adv_str = ','.join(map(to_int_str,np.random.uniform(mean-variance,mean+variance,samples)))
        print(adv_str, samples)
        print(np.random.uniform(mean-variance,mean+variance,samples))
        # tmp_file = get_me_a_tmp_file()
        # print("python allocation_with_freq.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta_dict, web_page_freq_sorted, adv_str,tmp_file,j))
        # os.system("python allocation_with_freq.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta_dict, web_page_freq_sorted, adv_str,tmp_file,j))
        # print("AD REPEATABILITY OF OUR NEW METHOD : "+str(advertiser_length))
        # with open(tmp_file,'r') as f:
        #     PVC = f.readline().strip()
        #     AAS = f.readline().strip()
        # # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json")
        # output = os.popen("python ad_repeatability_random_alloc.py {0} ./new_alloc_web_page_to_adv.json".format(transactional_data)).read()
        # print(output)
        # alloc = len(json.load(open("./allocated_adslots.json")))
        # adrep = filter(len,output.split('\n'))[0]
        # new_method.append(str(advertiser_length)+"_"+str(k)+"_"+str(j)+":"+str(alloc)+"_"+str(PVC)+"_"+str(adrep)+"_"+str(AAS))
        #
        tmp_file = get_me_a_tmp_file()
        # print("ALLOCATING WITH ONESLOT METHOD: "+str(advertiser_length))
        # os.system("python allocation_oneslot1.py {0} {1} {2} {3} {4}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file))
        # print("AD REPEATABILITY OF ONE SLOT METHOD : "+str(advertiser_length))
        # # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json")
        # # output = os.popen('python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv_oneslot.json').read()
        # output = os.popen("python ad_repeatability_random_alloc.py {0} ./new_alloc_web_page_to_adv_oneslot.json".format(transactional_data)).read()
        # print(output)
        # alloc = len(json.load(open("./allocated_adslots_oneslot.json")))
        # adrep = float(filter(len,output.split('\n'))[0])
        # ad_repeatability['oneslot_method'].append(adrep)
        # allocation['oneslot_method'].append(alloc)
        # ad_rep_per_alloc['oneslot_method'].append(adrep/alloc)
        print("python allocation_oneslot1.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file,j))
        os.system("python allocation_oneslot1.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file,j))
        print("AD REPEATABILITY OF ONE-SLOT METHOD : "+str(advertiser_length))
        with open(tmp_file,'r') as f:
            PVC = f.readline().strip()
            AAS = f.readline().strip()
        # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json")
        output = os.popen("python ad_repeatability_random_alloc.py {0} ./new_alloc_web_page_to_adv.json".format(transactional_data)).read()
        print(output)
        alloc = len(json.load(open("./allocated_adslots.json")))
        adrep = filter(len,output.split('\n'))[0]
        print("allocated : "+str(alloc))
        oneslot_method.append(str(advertiser_length)+"_"+str(k)+"_"+str(j)+":"+str(alloc)+"_"+str(PVC)+"_"+str(adrep)+"_"+str(AAS))
        # tmp_file = get_me_a_tmp_file()
        # print("ALLOCATING WITH RANDOM METHOD: "+str(advertiser_length))
        # print("python random_allocation.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file,j))
        # os.system("python random_allocation.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file,j))
        # print("AD REPEATABILITY OF RANDOM METHOD: "+str(advertiser_length))
        # # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./random_alloc_web_page_to_adv.json ")
        # with open(tmp_file,'r') as f:
        #     PVC = f.readline().strip()
        #     AAS = f.readline().strip()
        # # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json")
        # output = os.popen("python ad_repeatability_random_alloc.py {0} ./random_alloc_web_page_to_adv.json".format(transactional_data)).read()
        # print(output)
        # alloc = len(json.load(open("./random_allocated_adslots.json")))
        # adrep = filter(len,output.split('\n'))[0]
        # VFS_method.append(str(advertiser_length)+"_"+str(k)+"_"+str(j)+":"+str(alloc)+"_"+str(PVC)+"_"+str(adrep)+"_"+str(AAS))
    # with open("mslot.txt",'w') as f:
    #     for line in new_method:
    #         f.write(line+"\n")
    with open("oneslot.txt",'w') as f:
        for line in oneslot_method:
            f.write(line+"\n")
    # with open("vfs.txt",'w') as f:
    #     for line in VFS_method:
    #         f.write(line+"\n")

# new_method =[]
# oneslot_method =[]
# VFS_method=[]
# with open("mslot.txt",'w') as f:
#     for line in new_method:
#         f.write(line+"\n")
with open("oneslot.txt",'w') as f:
    for line in oneslot_method:
        f.write(line+"\n")
# with open("vfs.txt",'w') as f:
#     for line in VFS_method:
#         f.write(line+"\n")
        

# print(ad_repeatability)
# print(allocation)
# plt.clf()
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.scatter(advertiser_lengths,ad_repeatability['new_method'], label="New Method")
# ax1.scatter(advertiser_lengths,ad_repeatability['oneslot_method'], label="oneslot")
# ax1.scatter(advertiser_lengths,ad_repeatability['vfs'], label="VFS")
# plt.legend(loc="upper left")
# plt.xlabel("Advertisers Data Length")
# plt.ylabel("Ad Repeatability")
# plt.savefig("./ad_rep_kosark.png")
# plt.clf()
# plt.cla()
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.scatter(advertiser_lengths,allocation['new_method'],label="New Method")
# ax1.scatter(advertiser_lengths,allocation['oneslot_method'],label="oneslot")
# ax1.scatter(advertiser_lengths,allocation['vfs'],label="VFS")
# plt.xlabel("Advertisers Data Length")
# plt.ylabel("Ad Allocation")
# plt.legend(loc="upper left")
# plt.savefig("./ad_alloc_kosark.png")

# plt.clf()
# plt.cla()
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.scatter(advertiser_lengths,ad_rep_per_alloc['new_method'],label="New Method")
# ax1.scatter(advertiser_lengths,ad_rep_per_alloc['oneslot_method'],label="oneslot")
# ax1.scatter(advertiser_lengths,ad_rep_per_alloc['vfs'],label="VFS")
# plt.xlabel("Advertisers Data Length")
# plt.ylabel("Ad Rept. Per Alloc")
# plt.legend(loc="upper left")
# plt.savefig("./ad_rep_per_alloc_kosark.png")
