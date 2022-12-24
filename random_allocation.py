import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict


# PATTERNS_FILE_PATH = sys.argv[1]
META_DATA_FILE_PATH = sys.argv[2]
print("META_DATA_FILE_PATH", META_DATA_FILE_PATH)
# FREQ_SORT_DATA_FILE_PATH = sys.argv[2]
DELTA = int(sys.argv[6])
data_return_file_path = sys.argv[5]#"views_wasted1.txt"

with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)

DATA_FILE_PATH = sys.argv[7]
data_file = open(DATA_FILE_PATH,'r')


web_page_meta_dict2 = dict(web_page_meta_dict)

total_views_rem=0
for key in web_page_meta_dict:
    # if web_page_meta_dict2[key]['frequency'] < 0.02*100000 :#< 5445:#> 4000 and web_page_meta_dict2[key]['frequency'] < 9000 : #> 4000 and web_page_meta_dict2[key]['frequency'] < 9000:
    #     del web_page_meta_dict2[key]
    #     continue
    # else:
    total_views_rem+=(web_page_meta_dict[key]['frequency']*web_page_meta_dict[key]['ad_slots'])

web_page_meta_dict = web_page_meta_dict2
webpage_user_dict = {}

# transaction_num=0
# for transaction in data_file:
#     transaction_num+=1
#     web_page_list = transaction.strip().split(" ")
#     for web_page in web_page_list:
#         # if web_page_meta_dict[web_page]['frequency'] < 300:
#         #     continue
#         if web_page not in webpage_user_dict:
#             webpage_user_dict[web_page]=set([transaction_num])
#         else:
#             webpage_user_dict[web_page].add(transaction_num)
# 0.47026
# adslots_meta_dict = {}
# okok = []
# for web_page in web_page_meta_dict:
#     okok.append(int(web_page_meta_dict[web_page]['ad_slots']))
#     permutations_list = [web_page+"_"+str(freq) for freq in range(1,web_page_meta_dict[web_page]['ad_slots']+1) ]
#     for permutation in permutations_list:
#         # print(permutation)
#         adslots_meta_dict[permutation] = dict(web_page_meta_dict[web_page])
#         adslots_meta_dict[permutation]['webpage']=web_page
        
# okok.sort()
# print("limit {} to {}".format(okok[0],okok[-1]))
# exit()
advertisers_data = map(int,sys.argv[4].split(','))#[random.randint(220100,400100) for i in range(ADVERTISERS_DATA_LENGTH)]
advertisers_data.sort(reverse=True)
ADVERTISERS_DATA_LENGTH = len(advertisers_data)
advertisers_failed = []
advertisers_success = defaultdict(list)
advertisers_freq_req = [0]*ADVERTISERS_DATA_LENGTH
WEB_PAGES_COUNT = len(web_page_meta_dict)
# AD_SLOTS_COUNT = len(adslots_meta_dict)
# ad_slots = adslots_meta_dict.keys()
allocated_lookup = set()

# def getRandomWebPage():
#     random_ad_slot_index = random.choice(adslots_meta_dict.keys())
#     return random_ad_slot_index

# def get_web_page_from_ad_slot(ad_slot):
#     return ad_slot.split('_')[0]

# def get_min_max(patterns):
#     return min(map(lambda x: patterns[x]['frequency'],patterns.keys())),max(map(lambda x: patterns[x]['frequency'],patterns.keys()))

captured_revenue = 0
total_revenue = sum(advertisers_data)
web_page_to_advertiser = defaultdict(list)
i = 0
no_of_allocated = 0
views_wasted=0
curtotal_views=0
sum_of_scaled_allocated_impressions = 0
# for i, advertisers_req in enumerate(advertisers_data):
web_page_set=set()
web_page_set.clear()

final_failed = []

for i, required_coverage_support in enumerate(advertisers_data):
    # print("reallocating  {}".format(failed))
    # print("remaining web pages: {}".format(len(web_page_meta_dict)))
    current_allocation = set()
    allocated_adslots = []
    deleted_web_pages = {}
    while len(current_allocation) < required_coverage_support and len(web_page_meta_dict) > 0:
        # i = failed['i']
        cur_web_page = random.choice(web_page_meta_dict.keys())
        allocated_ad_slot = cur_web_page + "_" + str(web_page_meta_dict[cur_web_page]['ad_slots'])
        allocated_adslots.append(allocated_ad_slot)
        current_allocation=current_allocation.union(web_page_meta_dict[cur_web_page]['transactions'])
        web_page_to_advertiser[cur_web_page].append(i)
        web_page_meta_dict[cur_web_page]['ad_slots'] -= 1
        if web_page_meta_dict[cur_web_page]['ad_slots'] == 0:
            # if cur_web_page not in deleted_web_pages:
            #     deleted_web_pages[cur_web_page] = dict(web_page_meta_dict[cur_web_page])
            # deleted_web_pages[cur_web_page]['ad_slots'] += 1
            del web_page_meta_dict[cur_web_page]
    if len(current_allocation) < required_coverage_support:
        final_failed.append({'req':required_coverage_support,'i':i})
        # web_page_meta_dict.update(deleted_web_pages)
        # print("ReAllocation failed for {} , got only {}".format(required_coverage_support, len(current_allocation)))
        continue
    captured_revenue += required_coverage_support
    no_of_allocated += 1

# while i< ADVERTISERS_DATA_LENGTH and len(adslots_meta_dict) > 0 :
#     # print("patterns left: {} {} allocation:{}".format(len(adslots_meta_dict),advertisers_data[i],i))
#     allocated_ad_slot_index  = getRandomWebPage()
#     # print(allocated_ad_slot_index)
#     curtotal_views+=web_page_meta_dict[adslots_meta_dict[allocated_ad_slot_index]['webpage']]['frequency']
#     web_page_set=web_page_set.union(web_page_meta_dict[str(adslots_meta_dict[allocated_ad_slot_index]['webpage'])]['transactions'])
#     # advertisers_freq_req[i] += adslots_meta_dict[allocated_ad_slot_index]['frequency']
#     advertisers_success[i].append(adslots_meta_dict[allocated_ad_slot_index])
#     allocated = False
#     # cur_min,cur_max = get_min_max(adslots_meta_dict)
#     # print("i: {} required: {} cur_allocated: {} total_allocated: {}, Min: {} , Max: {}".format(i,advertisers_data[i],adslots_meta_dict[allocated_ad_slot_index]['frequency'],advertisers_freq_req[i],cur_min, cur_max))
#     if len(web_page_set) >= advertisers_data[i]:#*(100-DELTA)*1.0/100.0:
#         captured_revenue += advertisers_data[i]
#         views_wasted+=(curtotal_views-len(web_page_set))
#         total_views_rem-=curtotal_views
#         curtotal_views=0
#         sum_of_scaled_allocated_impressions += max(1.0,advertisers_freq_req[i]/advertisers_data[i])
#         allocated = True
#         no_of_allocated += 1
#         # print("allocated")
        
#     del adslots_meta_dict[allocated_ad_slot_index]
#     # print("len:{}".format(len(adslots_meta_dict.keys())))
#     web_page_to_advertiser[get_web_page_from_ad_slot(allocated_ad_slot_index)].append(i)
#     if allocated:
#         i += 1
#         web_page_set.clear() 

# PRC = captured_revenue*100.0/total_revenue

# allocated_impressions = sum_of_scaled_allocated_impressions
# AAS = allocated_impressions*10.0/len(advertisers_data)

print(data_return_file_path)
with open(data_return_file_path,'a') as f:
    f.write(str(ADVERTISERS_DATA_LENGTH)+" "+str(views_wasted)+" "+str(total_views_rem)+" "+str(captured_revenue)+"\n")
    # f.write(str(AAS)+"\n")

# print("Allocation accuracy: "+str(len(advertisers_success)))
print("Allocation accuracy: "+str(no_of_allocated))
print("total views sold: "+ str(captured_revenue))
with open(sys.argv[8],'w') as f:
    json.dump(advertisers_success,f)

with open(sys.argv[9],'w') as f:
    json.dump(web_page_to_advertiser,f)
