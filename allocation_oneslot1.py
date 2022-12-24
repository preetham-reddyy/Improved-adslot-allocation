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
advertisers_data = map(int,sys.argv[4].split(','))
advertisers_data.sort(reverse=True)
data_return_file_path = sys.argv[5]
total_revenue =sum(advertisers_data)
captured_revenue=0
avg_user_rating=0
# ADVERTISERS_DATA_LENGTH = int(sys.argv[4])
DELTA=int(sys.argv[6])

with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)

for web_page in web_page_meta_dict:
    web_page_meta_dict[web_page]['remaining'] = web_page_meta_dict[web_page]['ad_slots'] 

with open(FREQ_SORT_DATA_FILE_PATH,'r') as f:
    web_page_freq_sorted = pickle.load(f)


with open(PATTERNS_FILE_PATH) as f:
    patterns_file_data = f.readlines()


def getUniqueness(string, last_pattern_item_freq, debug,items):
    try:
        q = int(string[1:int(string[0])+1])
        r = int(string[int(string[0])+2:])
        ovr = r*100000.0/last_pattern_item_freq
        return abs(ovr-q), q
    except Exception as e:
        print("ERROR:")
        print(e)
        print(string,last_pattern_item_freq)
        print(debug)
        print(items)
        sys.exit(1)

patterns_file_data = [x.strip() for x in patterns_file_data]

web_page_to_pattern_map = defaultdict(list)
patterns = []

def get_ad_slot_item(pattern, index):
    # global web_page_to_pattern_map
    
    # print(pattern,index)
    items = re.findall("\d+", pattern)
    pattern_list = items[:-1]
    cmine_metadata = items[-1]
    
    uniqueness, coverage_support = getUniqueness(cmine_metadata, web_page_meta_dict[pattern_list[-1]]['frequency'],index,pattern)
    del items
    pattern_freq = 0
    
    for item in pattern_list:
        # web_page_to_pattern[item].append(index)
        pattern_freq = pattern_freq + web_page_meta_dict[item]['frequency']
    

    pattern_dict = {}

    for web_page in pattern_list:
        pattern_dict[web_page] = True
        # web_page_to_pattern_map[web_page].append(index)

    return {
        'pattern': pattern_dict, # {'1':true, '2':true}
        'pattern_freq': pattern_freq,
        'uniqueness': uniqueness,
        'coverage_support': coverage_support,
        'deleted':False
    }



patterns = [get_ad_slot_item(pattern, index) for index, pattern in enumerate(patterns_file_data)]
patterns.sort(key=lambda x: (x['pattern_freq']), reverse=True)

for index, pattern in enumerate(patterns):
    pattern_list = pattern['pattern']
    for web_page in pattern_list:
        web_page_to_pattern_map[web_page].append(index)

# import pdb; pdb.set_trace()
# print(len(web_page_to_pattern_map))
# sys.exit(1)
# _to_pattern = defaultdict(list)

# 1 => 2 slots 
# 2 => 2 slots

# 1,2 is a pattern

# pattern => [1,2] ... {1:True,2:True}
# for pattern in patterns:
#     # [[1_1,1_2],[2_1,2_2],[3_1,3_2]]
#     # permutations_list = [[item for freq in range(1,2)] for item in pattern['pattern']]
#     # permutations_list = [[item] for item in pattern['pattern']]
#     # permutations = list(itertools.product(*permutations_list))
#     # print(permutations)
#     new_pattern = dict(pattern)
#     new_pattern['pattern'] = {}
#     for web_page in pattern['pattern']:
#         new_pattern['pattern'][web_page] = True
#         web_page_to_pattern_map[web_page].append(len(patterns))
#     # 0..
#     patterns.append(new_pattern)

    # for permutation in permutations:
    #     new_pattern = dict(pattern)
    #     new_pattern['pattern'] = {} 
    #     for i in range(len(permutation)):
    #         new_pattern['pattern'][permutation[i]] = True
    #         web_page_to_pattern_map[permutation[i]].append(len(patterns))
    #     patterns.append(new_pattern)

# def binary_search_on_patterns_helper(arr, l, r, x):
#     if r >= l: 
#         mid = l + (r - l) // 2
#         # print(l,r,mid,arr[mid]['coverage_support'])

#         if arr[mid]['deleted']:
#             left_ans = binary_search_on_patterns_helper(arr,l,mid-1,x)
#             if left_ans:
#                 return left_ans
#             return binary_search_on_patterns_helper(arr,mid+1,r,x)
#         if mid == 0:
#             if arr[mid]['coverage_support'] >= x :
#                return mid
#             elif r==mid+1 and arr[r]['coverage_support'] >= x:
#                 return r
#             else:
#                 return None
        
#         if arr[mid]['coverage_support'] >= x and  arr[mid-1]['coverage_support'] < x: 
#             return mid 
#         elif arr[mid]['coverage_support'] >= x: 
#             return binary_search_on_patterns_helper(arr, l, mid-1, x) 
#         else: 
#             return binary_search_on_patterns_helper(arr, mid + 1, r, x) 
  
#     else: 
#         return None

# def binary_search_on_patterns(arr,x):
#     return binary_search_on_patterns_helper(arr,0,len(arr)-1,x)
def linear_search_on_patterns(arr,x):
    i = 0
    ans=None
    for item in arr:
        if item['deleted']:
            i+=1
            continue
        if item['pattern_freq'] >=x*(1.0-((DELTA*1.0)/100.0)):
            ans=i
        else:
            break
        i+=1
    return ans
# def linear_search_on_patterns(arr,x):
#     # i = 0
#     ans =  None
#     for index, item in enumerate(arr):
#         if item['deleted']:
#             continue
#         if abs(x - item['pattern_freq']) <= x*DELTA/100:
#             # print(index)
#             # return index
#             ans = index
#         elif ans is not None:
#             break
#     return ans

# def get_web_page_from_ad_slot(ad_slot):
#     return ad_slot.split('_')[0]

# print(patterns[:5])
# print(patterns[-5:])
# print(len(patterns))
# advertisers_data = [random.randint(220100,400100) for i in range(ADVERTISERS_DATA_LENGTH)]

advertisers_failed = []
advertisers_success = {}
web_page_to_advertiser = defaultdict(list)

for i, advertisers_req in enumerate(advertisers_data):
    # global web_page_to_pattern_map
    # print("Avialable Patterns:"+str(len([p  for p in patterns if p['deleted']==False] )))
    # print(patterns[:10])
    
    required_coverage_support = advertisers_req
    allocated_index = linear_search_on_patterns(patterns,required_coverage_support)

    # print("Requesting CS:"+str(required_coverage_support))
    if allocated_index == None:
        # import pdb; pdb.set_trace()
        advertisers_failed.append(advertisers_req)
        # print(" Allocation failed")
        continue
    
    captured_revenue += required_coverage_support
    # print("{0} vadki index:{1} pattern allocate ayindhi".format(i,allocated_index))
    # print(patterns[allocated_index])
    # print("required:"+str(required_coverage_support)+" alloc:"+str(patterns[allocated_index]['pattern_freq']))
    allocated_web_pages = list(patterns[allocated_index]['pattern'])
    # patterns[allocated_index]['deleted'] = True
    # print(" ALLOCATED:"+str(patterns[allocated_index]['coverage_support'])+"  " +" ".join(patterns[allocated_index]['pattern']))
    # print(required_coverage_support,patterns[allocated_index]['coverage_support'])
    advertisers_success[i] = dict(patterns[allocated_index])
    advertisers_success[i]['requirement'] = required_coverage_support
    advertisers_success[i]['allocated_adslots'] = []

    for web_page in allocated_web_pages:
        allocated_ad_slot = web_page + "_" + str(web_page_meta_dict[web_page]['remaining'])
        advertisers_success[i]['allocated_adslots'].append(allocated_ad_slot)
        web_page_meta_dict[web_page]['remaining'] -= 1
        web_page_to_advertiser[web_page].append(i)
        if web_page_meta_dict[web_page]['remaining'] == 0:
            removing_patterns = web_page_to_pattern_map[web_page]
            for pattern in removing_patterns:
                
                # if pattern == allocated_index:
                #     continue
                if web_page in patterns[pattern]['pattern']:

                    # Motham pattern ni delete cheyali antey
                    # patterns[pattern]['deleted'] = True
                    del patterns[pattern]['pattern'][web_page]
                    patterns[pattern]['pattern_freq'] -= web_page_meta_dict[web_page]['frequency']  
                else:
                    # import pdb; pdb.set_trace()
                    print("ERRRORR")
                    print(web_page)
                    print(patterns[pattern]['pattern'])
            web_page_to_pattern_map[web_page] = []

        # removing_patterns = web_page_to_pattern_map[ad_slot]
        # # print("removing patterns"+str(len(removing_patterns)))
        # # print(get_web_page_from_ad_slot(ad_slot))
        # web_page_to_advertiser[get_web_page_from_ad_slot(ad_slot)].append(i)
        # for pattern in removing_patterns:
        #     if pattern == allocated_index:
        #         continue
        #     if ad_slot in patterns[pattern]['pattern']:
        #         del patterns[pattern]['pattern'][ad_slot]
        #         patterns[pattern]['pattern_freq'] -= web_page_meta_dict[get_web_page_from_ad_slot(ad_slot)]['frequency']
    
    patterns.sort(key=lambda x: (x['pattern_freq']),reverse=True)
    web_page_to_pattern_map = defaultdict(list)
    for index, pattern in enumerate(patterns):
        pattern_list = pattern['pattern']
        for web_page in pattern_list:
            web_page_to_pattern_map[web_page].append(index)
    # web_page_to_advertiser[get_web_page_from_ad_slot(allocated_index)].append(i)
PRC = captured_revenue*100.0/total_revenue

allocated_impressions = sum([max(1.0,advertisers_success[x]['pattern_freq']/advertisers_success[x]['requirement']) for x in advertisers_success])
AAS = allocated_impressions*10.0/len(advertisers_data)

with open(data_return_file_path,'w') as f:
    # print("heyy")
    # print(data_return_file_path)
    
    f.write(str(PRC)+"\n")
    f.write(str(AAS)+"\n")
# print(PRC)
print("Allocation accuracy new method: "+str(len(advertisers_success)))

with open("allocated_adslots.json",'w') as f:
    json.dump(advertisers_success,f)

with open("new_alloc_web_page_to_adv.json",'w') as f:
    json.dump(web_page_to_advertiser,f)
