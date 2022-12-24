from __future__ import print_function
import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict
from multiprocessing import Pool

PATTERNS_FILE_PATH = sys.argv[1]
META_DATA_FILE_PATH = sys.argv[2]
FREQ_SORT_DATA_FILE_PATH = sys.argv[3]
advertisers_data = map(int,sys.argv[4].split(','))
advertisers_data.sort(reverse=True)
data_return_file_path = sys.argv[5]
DELTA=int(sys.argv[6])
MIN_RF = 0.02

with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)

for web_page in web_page_meta_dict:
    web_page_meta_dict[web_page]['remaining'] = web_page_meta_dict[web_page]['ad_slots'] 

with open(FREQ_SORT_DATA_FILE_PATH,'r') as f:
    web_page_freq_sorted = pickle.load(f)


with open(PATTERNS_FILE_PATH) as f:
    patterns_file_data = f.readlines()

def get_ad_slot_item(index, pattern):
    values = pattern.split('|')
    items = values[0].split(', ')
    items = [int(item.strip()) for item in items]
    pattern_list = items
    pattern_set = set(pattern_list)
    coverage_support = float(values[1].strip())
    overlap_ratio = float(values[2].strip())
    p =  {
        'pattern': pattern_set,
        'coverage_support': coverage_support,
        'overlap_ratio': overlap_ratio,
    }
    return p
    
def get_ad_slot_item_proxy(args): # (1, [1,2,3])
    return get_ad_slot_item(*args)

p = Pool(29)
patterns = p.map(get_ad_slot_item_proxy, enumerate(patterns_file_data)) 
print("got patterns")
patterns.sort(key=lambda x: x['coverage_support'], reverse=True)
print("sorted patterns")

# for i in patterns:
#     print(i['pattern'],i['coverage_support'])
# print(patterns)

web_page_to_pattern_map = defaultdict(list)
# print(patterns)
for index, pattern in enumerate(patterns):
    pattern_list = pattern['pattern']
    for web_page in pattern_list:
        web_page_to_pattern_map[web_page].append(index)
        
# print(web_page_to_pattern_map)
def linear_search_on_patterns(arr, required):
    ans = None
    for index, item in enumerate(arr):
        if item['coverage_support'] >= required:
            ans = index
            continue
        elif ans is not None:
            break
        ans = index
        break
    return ans

lower_than_minrf_webpages =  map(lambda x: x[0], list(filter(lambda x: x[1] < MIN_RF*100000, web_page_freq_sorted)))

# print("chec")
# print("check2",len(lower_than_minrf_webpages))
advertisers_failed = []
advertisers_success = {}
web_page_to_advertiser = defaultdict(list)

views_wasted=0
s=""
cnt=0
ad_len=len(advertisers_data)
print("started allocation")
# print("advertisers_data", advertisers_data)
revenue = 0
for i, advertisers_req in enumerate(advertisers_data):
    #global web_page_to_pattern_map
    #print("required", advertisers_req)
    required_coverage_support = advertisers_req
    allocated_index = linear_search_on_patterns(patterns,required_coverage_support)
    allocated_value = 0 if allocated_index is None else patterns[allocated_index]['coverage_support']
    allocated_webpages = patterns[allocated_index]['pattern'] if allocated_index is not None else set()
    is_allocation_fine = allocated_value >= required_coverage_support
    #print("patterns nunchi allocate ayindha", allocated_value, is_allocation_fine, allocated_index)
    #if allocated_index:
        #print("allocated pattern", patterns[allocated_index]['pattern'])
    if not is_allocation_fine: #print("allocating with low minrf pages")
        rem_low_pages = list(lower_than_minrf_webpages)
        current_allocation=set()
        if allocated_index is not None:
            for page in patterns[allocated_index]['pattern']:
                current_allocation=current_allocation.union(web_page_meta_dict[str(page)]['transactions'])
        # Allocate from lower_than_minrf_webpages
        while allocated_value < required_coverage_support and len(rem_low_pages) > 0:
            cur_web_page = random.choice(range(len(rem_low_pages)))
            # print("check", allocated_value , required_coverage_support, len(rem_low_pages),rem_low_pages[cur_web_page], web_page_meta_dict[rem_low_pages[cur_web_page]]['ad_slots'])
            # print("cur_web_page", cur_web_page)
            # print("rem_low_pages[cur_web_page]", rem_low_pages[cur_web_page])
            current_allocation = current_allocation.union(set(web_page_meta_dict[rem_low_pages[cur_web_page]]['transactions']))
            allocated_webpages.add(rem_low_pages[cur_web_page])
            web_page_meta_dict[rem_low_pages[cur_web_page]]['ad_slots'] -= 1
            if web_page_meta_dict[rem_low_pages[cur_web_page]]['ad_slots'] <= 0:
                # print("dleeting")
                del rem_low_pages[cur_web_page]
            allocated_value = len(current_allocation)
        is_allocation_fine = allocated_value >= required_coverage_support
        if is_allocation_fine:
#            print("allocated with low pages")
            lower_than_minrf_webpages=rem_low_pages
#print("web pages ayyasarki allocate ayindha", is_allocation_fine, allocated_value)
    if not is_allocation_fine:
#        print("allocation failed, tried all things")
        continue
    else:
        revenue += advertisers_req
        cnt += 1
    advertisers_success[i]={'allocated_adslots':[]}
    # print("allocated web_pages", allocated_webpages)
    # print("patterns allocated index", patterns[allocated_index])
    # print(web_page_to_pattern_map)
    removing_patterns = set()
    for webpage in allocated_webpages:
        # print("removing webpage", webpage)
        # print(web_page_meta_dict)
        if webpage in web_page_to_pattern_map:
            # print("remaining adslots", web_page_meta_dict[str(webpage)]['remaining'])
            web_page_meta_dict[str(webpage)]['remaining'] -= 1
            # print("remaining adslots", web_page_meta_dict[str(webpage)]['remaining'])
        allocated_ad_slot = str(webpage) + "_" + str(web_page_meta_dict[str(webpage)]['remaining'])
        advertisers_success[i]['allocated_adslots'].append(allocated_ad_slot)
        web_page_to_advertiser[webpage].append(i)
        # print(len(patterns))
        if web_page_meta_dict[str(webpage)]['remaining'] == 0 and webpage in web_page_to_pattern_map:
            removing_patterns = removing_patterns.union(web_page_to_pattern_map[webpage])
            # print("removing patterns", removing_patterns)
            # print("reverse sorted", sorted(removing_patterns, reverse = True))
            # for i in range(5):
            #     print("removing", patterns[removing_patterns[i]])
            # print(patterns)
    removing_patterns = list(sorted(list(removing_patterns), reverse = True))
    for pattern_index in removing_patterns:
                # for w in patterns[pattern_index]['pattern']:
                #     if w not in web_page_to_pattern_map or len(web_page_to_pattern_map[w]) == 0:
        # print(patterns)
        # print(pattern_index) 
        del patterns[pattern_index]
                # print("patterns", patterns[pattern_index])
            # web_page_to_pattern_map[web_page] = []
    
    patterns.sort(key=lambda x: x['coverage_support'],reverse=True)
    web_page_to_pattern_map = defaultdict(list)
    for index, pattern in enumerate(patterns):
        pattern_list = pattern['pattern']
        for web_page in pattern_list:
            web_page_to_pattern_map[web_page].append(index)
    # print("web_page_to_pattern_map",web_page_to_pattern_map[webpage])

print("Allocation accuracy: "+str(cnt))

with open(data_return_file_path,'a') as f:
    # print("heyy")
    # print(data_return_file_path)
    # views_wasted=0
    f.write(str(ad_len)+" "+str(views_wasted)+" "+str(cnt)+"\n")
    # f.write(str(ad_len)+" "+str(views_wasted)+" "+str(total_views_rem)+" "+str(captured_revenue)+"\n")
    # f.write(str(AAS)+"\n")str(ad_len)+" "+str(views_wasted)+" "+str(total_views_rem)+" "+
    # print(PRC)

with open("allocs.txt",'a') as f:
    f.write(s)
print("total views sold: "+str(revenue))
print("Allocation accuracy new method: "+str(len(advertisers_success)))
# print("views wasted:"+str(views_wasted))
with open(sys.argv[7],'w') as f:
    json.dump(advertisers_success,f)

with open(sys.argv[8],'w') as f:
    json.dump(web_page_to_advertiser,f)
