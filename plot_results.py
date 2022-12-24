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
advertiser_lengths = [int(sys.argv[3])] 
# advertiser_lengths = [800]
# cmine tharvatha vachina file
if len(sys.argv) < 3:
    print("Sarriga arguments ichi dobichuko")
    os.exit(1)
# else:
    # PATTERNS_FILE_PATH = "../test1/dataset_bms_pos.txt_0.065_0.0_0.6_output.txt"
PATTERNS_FILE_PATH = sys.argv[1] #
# kindha advertisers data generate cheyadanki
ar1= int(sys.argv[4]) #6000 #8854 #int(sys.argv[2])
mean_list = [ar1]*len(advertiser_lengths)

print("###############     ARGUMENTS     ############")
print(sys.argv)
print("##############################################")

DATA_FILE_PATH = sys.argv[2]
dataset_name = ''.join([i for i in DATA_FILE_PATH.split('/')[-1] if i.isalpha()])

# build_meta_data.py nunchi vachina two files
DELTA=[2] #, 4, 6, 8, 10]

MIN_RF = 297

web_page_freq_one  = "/home/preetham_sathineni/adslot/web_page_freq_sorted_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[1])),dataset_name)
web_page_meta_one  = "/home/preetham_sathineni/adslot/web_page_meta_dict_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[1])),dataset_name)


# print(web_page_freq_one)
# print(web_page_meta_one)
# idhi mana transactional data (dataset)
transactional_data = DATA_FILE_PATH

allocated = {'new_method':[],'oneslot_method':[],'VFS_one_method':[],'VFS_multi_method':[]}
adrepp = {'new_method':[],'oneslot_method':[],'VFS_one_method':[],'VFS_multi_method':[]}
revenue = {'new_method':[],'oneslot_method':[],'VFS_one_method':[],'VFS_multi_method':[]}


def to_int_str(value):
    return str(int(value))

def get_me_a_tmp_file():
    random_num = current_milli_time()
    tmp_file = "/tmp/{0}.txt".format(str(random_num))
    os.system("touch {0}".format(tmp_file))
    return tmp_file

def get_me_a_json_file():
    random_num = current_milli_time()
    tmp_file = "./{0}.json".format(str(random_num))
    os.system("touch {}".format(tmp_file))
    return tmp_file

web_page_to_adv_json_file = get_me_a_json_file()
allocated_adslots_file = get_me_a_json_file()

print("web_page_to_adv_json_file : {}".format(web_page_to_adv_json_file))
print("allocated_adslots_file: {}".format(allocated_adslots_file))

AD_SLOTS=[sys.argv[6]]
for k in AD_SLOTS:
    for j in DELTA:
        for i in range(len(advertiser_lengths)):
            web_page_freq_sorted  = "/home/preetham_sathineni/adslot/web_page_freq_sorted_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[k])),dataset_name)
            web_page_meta_dict  = "/home/preetham_sathineni/adslot/web_page_meta_dict_adslots_{0}_dataset_{1}.pkl".format("_".join(map(str,[k])),dataset_name)
            # print(web_page_freq_sorted)
            # exit()
            web_page_freq = web_page_freq_sorted
            web_page_meta = web_page_meta_dict
            # This is random distribution between min and max values
            # adv_str = ','.join(map(str,[random.randint(100000,250000) for i in range(advertiser_length)]))
            # this is uniform distribution for given mean and variance
            advertiser_length = advertiser_lengths[i]
            
            #ee block to generate advertisers data
            mean = mean_list[i]
            variance = int(sys.argv[5]) #4000 #(int)(9000/advertiser_lengths[i])
            samples = advertiser_length
            
            adv_str = ','.join(map(to_int_str,np.random.uniform(mean-variance,mean+variance,samples)))
            # print(adv_str, samples)
            # print(np.random.uniform(mean-variance,mean+variance,samples))

            ######################  MULTI SLOT CP METHOD ####################

            # print("ALLOCATING WITH OUR NEW METHOD: "+str(advertiser_length))

            tmp_file = get_me_a_tmp_file()

            print("python alloc_fresh.py {0} {1} {2} {3} {4} {5} {6} {7}".format(PATTERNS_FILE_PATH,web_page_meta_dict, web_page_freq_sorted, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file))
            os.system("python alloc_fresh.py {0} {1} {2} {3} {4} {5} {6} {7}".format(PATTERNS_FILE_PATH,web_page_meta_dict, web_page_freq_sorted, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file))
            # os.system("python allocation_with_reallocation.py {0} {1} {2} {3} {4} {5} {6} {7}".format(PATTERNS_FILE_PATH,web_page_meta_dict, web_page_freq_sorted, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file))
            
            print("AD REPEATABILITY OF OUR NEW METHOD : "+str(advertiser_length))
            # with open(tmp_file,'r') as f:
            #     revenue_captured = float(f.readline().strip().split()[-1])
            #     PVC = f.readline().strip()
            #     AAS = f.readline().strip()
                
            os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt "+ web_page_to_adv_json_file) #./new_alloc_web_page_to_adv.json")
            output = os.popen("python ad_repeatability_random_alloc.py {0} {1}".format(transactional_data, web_page_to_adv_json_file)).read()
            print(output)
            alloc = len(json.load(open(allocated_adslots_file)))
            adrep = filter(len,output.split('\n'))[0]

            # new_method.append(str(advertiser_length)+"_"+str(k)+"_"+str(j)+":"+str(alloc)+"_"+str(PVC)+"_"+str(adrep)+"_"+str(AAS))
            allocated['new_method'].append(alloc)
            adrepp['new_method'].append(adrep)
            # revenue['new_method'].append(revenue_captured)

            # ###################### ONE SLOT CP METHOD####################


            
            print("ALLOCATING WITH OUR OLD METHOD: "+str(advertiser_length))
            tmp_file = get_me_a_tmp_file()


            print("python alloc_fresh.py {0} {1} {2} {3} {4} {5} {6} {7}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file))
            os.system("python alloc_fresh.py {0} {1} {2} {3} {4} {5} {6} {7}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file))
            # print("python allocation_with_freq.py {0} {1} {2} {3} {4} {5}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j))
            # os.system("python allocation_with_freq_new.py {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file, MIN_RF))
            # os.system("python allocation_with_reallocation.py {0} {1} {2} {3} {4} {5} {6} {7}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j,allocated_adslots_file, web_page_to_adv_json_file))
            print("AD REPEATABILITY OF ONE-SLOT METHOD : "+str(advertiser_length))
            # with open(tmp_file,'r') as f:
            #     #PVC = f.readline().strip()
            #     #AAS = f.readline().strip()
                # revenue_captured = int(f.readline().strip().split()[-1])
            output = os.popen("python ad_repeatability_random_alloc.py {0} {1}".format(transactional_data, web_page_to_adv_json_file)).read()
            print(output)
            alloc = len(json.load(open(allocated_adslots_file)))
            adrep = filter(len,output.split('\n'))[0]
            allocated['oneslot_method'].append(alloc)
            adrepp['oneslot_method'].append(adrep)
            # revenue['oneslot_method'].append(revenue_captured)
            
            ######################## ONE SLOT RANDOM METHOD ####################

            tmp_file = get_me_a_tmp_file()

            print("[One slot] ALLOCATING WITH RANDOM METHOD: "+str(advertiser_length))
            # print("python random_allocation.py {0} {1} {2} {3} {4} {5} {6}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j,DATA_FILE_PATH))
            os.system("python random_allocation.py {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(PATTERNS_FILE_PATH,web_page_meta_one, web_page_freq_one, adv_str,tmp_file,j,DATA_FILE_PATH, allocated_adslots_file, web_page_to_adv_json_file))
            # print("AD REPEATABILITY OF RANDOM METHOD: "+str(advertiser_length))
            # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./random_alloc_web_page_to_adv.json ")
            # with open(tmp_file,'r') as f:
            #     #PVC = f.readline().strip()
            #     #AAS = f.readline().strip() 
                # revenue_captured = int(f.readline().strip().split()[-1])
            # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json")
            output = os.popen("python ad_repeatability_random_alloc.py {0} {1}".format(transactional_data, web_page_to_adv_json_file)).read()
            print(output)
            alloc = len(json.load(open(allocated_adslots_file)))
            adrep = filter(len,output.split('\n'))[0]
            
            # VFS_method.append(str(advertiser_length)+"_"+str(k)+"_"+str(j)+":"+str(alloc)+"_"+str(PVC)+"_"+str(adrep)+"_"+str(AAS))
            # VFS_method[allocated].append(alloc)
            # VFS_method[adrepeatability].append(adrep)  
            allocated['VFS_one_method'].append(alloc)
            adrepp['VFS_one_method'].append(adrep)
            # revenue['VFS_one_method'].append(revenue_captured)   


            #######################  MULTI SLOT RANDOM METHOD ####################

            tmp_file = get_me_a_tmp_file()

            print("[Multi slots] ALLOCATING WITH RANDOM METHOD: "+str(advertiser_length))
            # print("python random_allocation.py {0} {1} {2} {3} {4} {5} {6}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file,j,DATA_FILE_PATH))
            os.system("python random_allocation.py {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(PATTERNS_FILE_PATH,web_page_meta, web_page_freq, adv_str,tmp_file,j,DATA_FILE_PATH, allocated_adslots_file, web_page_to_adv_json_file))
            print("AD REPEATABILITY OF RANDOM METHOD: "+str(advertiser_length))
            # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./random_alloc_web_page_to_adv.json ")
            # with open(tmp_file,'r') as f:
            #     revenue_captured = int(f.readline().strip().split()[-1])
                # PVC = f.readline().strip()
                # AAS = f.readline().strip()
            # os.system("python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json")
            output = os.popen("python ad_repeatability_random_alloc.py {0} {1}".format(transactional_data, web_page_to_adv_json_file)).read()
            print(output)
            alloc = len(json.load(open(allocated_adslots_file)))
            adrep = filter(len,output.split('\n'))[0]
            
            # VFS_method.append(str(advertiser_length)+"_"+str(k)+"_"+str(j)+":"+str(alloc)+"_"+str(PVC)+"_"+str(adrep)+"_"+str(AAS))
            # VFS_method[allocated].append(alloc)
            # VFS_method[adrepeatability].append(adrep)  
            allocated['VFS_multi_method'].append(alloc)
            adrepp['VFS_multi_method'].append(adrep)  
            # revenue['VFS_multi_method'].append(revenue_captured)   

print("allocated")
print(allocated)
print("adrepp")
print(adrepp)
print("revenue")
print(revenue)
# f=open("./data_points/alloc1_{0}_{1}_{2}.txt".format(dataset_name,str(ar1),sys.argv[5]),'w')
# f.write("x y1 y2 y3 y4"+'\n')
# for i in range(0,len(advertiser_lengths)):
#     f.write(str(advertiser_lengths[i])+'  '+str(allocated['new_method'][i])+'  '+str(allocated['oneslot_method'][i])+'  '+str(allocated['VFS_one_method'][i])+'  '+str(allocated['VFS_multi_method'][i])+'\n')
# f.close()
# f=open("./data_points/adrep1_{0}_{1}_{2}.txt".format(dataset_name,str(ar1),sys.argv[5]),'w')
# f.write("x y1 y2 y3 y4"+'\n')
# for i in range(0,len(advertiser_lengths)):
#     f.write(str(advertiser_lengths[i])+'  '+str(adrepp['new_method'][i])+'  '+str(adrepp['oneslot_method'][i])+'  '+str(adrepp['VFS_one_method'][i])+'  '+str(adrepp['VFS_multi_method'][i])+'\n')
# f.close()
# f=open("./data_points/revenue_{0}_{1}_{2}.txt".format(dataset_name,str(ar1),sys.argv[5]),'w')
# f.write("x y1 y2 y3 y4"+'\n')
# for i in range(0,len(advertiser_lengths)):
#     f.write(str(advertiser_lengths[i])+'  '+str(revenue['new_method'][i])+'  '+str(revenue['oneslot_method'][i])+'  '+str(revenue['VFS_one_method'][i])+'  '+str(revenue['VFS_multi_method'][i])+'\n')
# f.close()
# plt.clf()
# fig = plt.figure()
# rng = np.arange(0, 0.6, 0.0005)
# ax1 = fig.add_subplot(111)
# ax1.plot(advertiser_lengths,adrepp['new_method'], label="New Method",marker = 'o')
# ax1.plot(advertiser_lengths,adrepp['oneslot_method'], label="oneslot",marker = 's')
# ax1.plot(advertiser_lengths,adrepp['VFS_one_method'],label="VFS_one",marker = 'X')
# ax1.plot(advertiser_lengths,adrepp['VFS_multi_method'],label="VFS_multi",marker = '^')
# ax1.set_yticks(rng)
# plt.legend(loc="upper left")
# plt.xlabel("Advertisers Data Length")
# plt.ylabel("Ad Repeatability")
# plt.savefig("./newadrep_{}.png".format(dataset_name))
# plt.clf()
# plt.cla()
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(advertiser_lengths,allocated['new_method'],label="New Method",marker = 'o')
# ax1.plot(advertiser_lengths,allocated['oneslot_method'],label="oneslot",marker = 's')
# ax1.plot(advertiser_lengths,allocated['VFS_one_method'],label="VFS_one",marker = 'X')
# ax1.plot(advertiser_lengths,allocated['VFS_multi_method'],label="VFS_multi",marker = '^')
# plt.xlabel("Advertisers Data Length")
# plt.ylabel("Ad Allocation")
# plt.legend(loc="upper left")
# plt.savefig("./newalloc_{}.png".format(dataset_name))



