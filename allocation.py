import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict

PATTERNS_FILE_PATH = sys.argv[1]
META_DATA_FILE_PATH = sys.argv[2]
FREQ_SORT_DATA_FILE_PATH = sys.argv[3]
ADVERTISERS_DATA_LENGTH = int(sys.argv[4])

with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)

with open(FREQ_SORT_DATA_FILE_PATH,'r') as f:
    web_page_freq_sorted = pickle.load(f)


with open(PATTERNS_FILE_PATH) as f:
    patterns_file_data = f.readlines()


def getUniqueness(string, last_pattern_item_freq):
    q = int(string[1:int(string[0])+1])
    r = int(string[int(string[0])+2:])
    ovr = r*100000.0/last_pattern_item_freq
    return abs(ovr-q), q

patterns_file_data = [x.strip() for x in patterns_file_data]


def get_ad_slot_item(pattern):
    items = re.findall("\d+", pattern)
    pattern_list = items[:-1]
    cmine_metadata = items[-1]
    del items
    uniqueness, coverage_support = getUniqueness(cmine_metadata, web_page_meta_dict[pattern_list[-1]]['frequency'])
    pattern_freq = 0
    
    for item in pattern_list:
        pattern_freq = pattern_freq + web_page_meta_dict[item]['frequency']
    
    return {
        'pattern': pattern_list,
        'pattern_freq': pattern_freq,
        'uniqueness': uniqueness,
        'coverage_support': coverage_support,
        'deleted':False
    }

patterns = [get_ad_slot_item(pattern) for pattern in patterns_file_data]
patterns.sort(key=lambda x: (x['coverage_support'], x['uniqueness']))
patterns_with_adslots = []


ad_slot_to_pattern_map = defaultdict(list)

for pattern in patterns:
    permutations_list = [[item+"_"+str(freq) for freq in range(1,web_page_meta_dict[item]['ad_slots']+1)] for item in pattern['pattern']]
    permutations = list(itertools.product(*permutations_list))
    # print(permutations)
    for permutation in permutations:
        new_pattern = dict(pattern)
        new_pattern['pattern'] = list(permutation)
        for i in range(len(permutation)):
            ad_slot_to_pattern_map[permutation[i]].append(len(patterns_with_adslots))
        patterns_with_adslots.append(new_pattern)

def binary_search_on_patterns_helper(arr, l, r, x):
    if r >= l: 
        mid = l + (r - l) // 2
        # print(l,r,mid,arr[mid]['coverage_support'])

        if arr[mid]['deleted']:
            left_ans = binary_search_on_patterns_helper(arr,l,mid-1,x)
            if left_ans == None:
                return binary_search_on_patterns_helper(arr,mid+1,r,x)
            else:
                return left_ans
        if mid == 0:
            if arr[mid]['coverage_support'] >= x :
               return mid
            elif r==mid+1 and arr[r]['coverage_support'] >= x:
                return r
            else:
                return None
        
        if arr[mid]['coverage_support'] >= x and  arr[mid-1]['coverage_support'] < x: 
            return mid 
        elif arr[mid]['coverage_support'] >= x: 
            return binary_search_on_patterns_helper(arr, l, mid-1, x) 
        else: 
            return binary_search_on_patterns_helper(arr, mid + 1, r, x) 
  
    else: 
        return None

def binary_search_on_patterns(arr,x):
    return binary_search_on_patterns_helper(arr,0,len(arr)-1,x)

def linear_search_on_patterns(arr,x):
    for i,item in enumerate(arr):
        if item['deleted']:
            continue
        if item['coverage_support'] >=x:
            return i
    return None

def get_web_page_from_ad_slot(ad_slot):
    return ad_slot.split('_')[0]

# print(patterns_with_adslots[:5])
# print(patterns_with_adslots[-5:])
# print(len(patterns_with_adslots))
advertisers_data = [random.randint(25100,100100) for i in range(ADVERTISERS_DATA_LENGTH)]
advertisers_failed = []
advertisers_success = {}
web_page_to_advertiser = defaultdict(list)
for i, advertisers_req in enumerate(advertisers_data):
    # print("Avialable Patterns:"+str(len([p  for p in patterns_with_adslots if p['deleted']==False] )))
    required_coverage_support = advertisers_req
    allocated_index = linear_search_on_patterns(patterns_with_adslots,required_coverage_support)
    # print("Requesting CS:"+str(required_coverage_support))
    if allocated_index == None:
        advertisers_failed.append(advertisers_req)
        # print(" FAILED")
        continue
    allocated_ad_slots = patterns_with_adslots[allocated_index]['pattern']
    # print(" ALLOCATED:"+str(patterns_with_adslots[allocated_index]['coverage_support'])+"  " +" ".join(patterns_with_adslots[allocated_index]['pattern']))
    # print(required_coverage_support,patterns_with_adslots[allocated_index]['coverage_support'])
    advertisers_success[i] = patterns_with_adslots[allocated_index]
    for ad_slot in allocated_ad_slots:
        removing_patterns = ad_slot_to_pattern_map[ad_slot]
        # print("removing patterns"+str(len(removing_patterns)))
        # print(get_web_page_from_ad_slot(ad_slot))
        web_page_to_advertiser[get_web_page_from_ad_slot(ad_slot)].append(i)
        for pattern in removing_patterns:
            
            patterns_with_adslots[pattern]['deleted'] = True
    
    # web_page_to_advertiser[get_web_page_from_ad_slot(allocated_index)].append(i)

print("Allocation accuracy: "+str(len(advertisers_success)))

with open("allocated_adslots.json",'w') as f:
    json.dump(advertisers_success,f)

with open("new_alloc_web_page_to_adv.json",'w') as f:
    json.dump(web_page_to_advertiser,f)