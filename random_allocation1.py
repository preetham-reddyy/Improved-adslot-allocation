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
# FREQ_SORT_DATA_FILE_PATH = sys.argv[2]
DELTA = int(sys.argv[6])
data_return_file_path = sys.argv[5]

with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)


adslots_meta_dict = {}
for web_page in web_page_meta_dict:
    permutations_list = [web_page+"_"+str(freq) for freq in range(1,web_page_meta_dict[web_page]['ad_slots']+1) ]
    for permutation in permutations_list:
        adslots_meta_dict[permutation] = dict(web_page_meta_dict[web_page])


advertisers_data = map(int,sys.argv[4].split(','))#[random.randint(220100,400100) for i in range(ADVERTISERS_DATA_LENGTH)]
advertisers_data.sort(reverse=True)
ADVERTISERS_DATA_LENGTH = len(advertisers_data)
advertisers_failed = []
advertisers_success = defaultdict(list)
advertisers_freq_req = [0]*ADVERTISERS_DATA_LENGTH
WEB_PAGES_COUNT = len(web_page_meta_dict)
AD_SLOTS_COUNT = len(adslots_meta_dict)
ad_slots = adslots_meta_dict.keys()
allocated_lookup = set()

def getRandomWebPageWithAdslot():
    random_web_page = random.randint(0,WEB_PAGES_COUNT-1)
    random_web_slot = random.randint(0,web_page_meta_dict[random_web_page]['ad_slots']-1)
    allocated_lookup_index = str(random_web_page)+"#"+str(random_web_slot)
    if allocated_lookup_index in allocated_lookup:
        return getRandomWebPageWithAdslot()
    allocated_lookup.add(allocated_lookup_index)
    return random_web_page,random_web_slot

def getRandomWebPage():
    random_ad_slot_index = random.choice(adslots_meta_dict.keys())
    # if random_ad_slot_index in allocated_lookup:
        # return getRandomWebPage()
    # allocated_lookup.add(random_ad_slot_index)
    
    return random_ad_slot_index


def get_web_page_from_ad_slot(ad_slot):
    return ad_slot.split('_')[0]

captured_revenue = 0
total_revenue = sum(advertisers_data)
web_page_to_advertiser = defaultdict(list)
i = 0
no_of_allocated = 0
sum_of_scaled_allocated_impressions = 0
# for i, advertisers_req in enumerate(advertisers_data):
while i< ADVERTISERS_DATA_LENGTH and len(adslots_meta_dict.keys()) > 0 :
    allocated_ad_slot_index  = getRandomWebPage()
    # print(allocated_ad_slot_index)
    advertisers_freq_req[i] += adslots_meta_dict[allocated_ad_slot_index]['frequency']
    advertisers_success[i].append(adslots_meta_dict[allocated_ad_slot_index])
    allocated = False
    if advertisers_freq_req[i] >= advertisers_data[i]:#*(100-DELTA)*1.0/100.0:
        captured_revenue += advertisers_data[i]
        sum_of_scaled_allocated_impressions += max(1.0,advertisers_freq_req[i]/advertisers_data[i])
        allocated = True
        no_of_allocated += 1
    del adslots_meta_dict[allocated_ad_slot_index]
    web_page_to_advertiser[get_web_page_from_ad_slot(allocated_ad_slot_index)].append(i)
    if allocated:
        i += 1

PRC = captured_revenue*100.0/total_revenue

allocated_impressions = sum_of_scaled_allocated_impressions
AAS = allocated_impressions*10.0/len(advertisers_data)

print(data_return_file_path)
with open(data_return_file_path,'w') as f:
    # print("heyy")
    # print(data_return_file_path)
    f.write(str(PRC)+"\n")
    f.write(str(AAS)+"\n")

# print("Allocation accuracy: "+str(len(advertisers_success)))
print("Allocation accuracy: "+str(no_of_allocated))

with open("random_allocated_adslots.json",'w') as f:
    json.dump(advertisers_success,f)

with open("random_alloc_web_page_to_adv.json",'w') as f:
    json.dump(web_page_to_advertiser,f)
