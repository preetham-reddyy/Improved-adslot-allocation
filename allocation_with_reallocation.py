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
# import multiset
from multiset import Multiset
import functools
import time
from multiprocessing import Pool




PATTERNS_FILE_PATH = sys.argv[1]
META_DATA_FILE_PATH = sys.argv[2]
FREQ_SORT_DATA_FILE_PATH = sys.argv[3]
advertisers_data = map(int,sys.argv[4].split(','))
advertisers_data.sort(reverse=True)
data_return_file_path = sys.argv[5]#"views_wasted.txt"
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

total_views_rem=0
for key in web_page_meta_dict:
    # if web_page_meta_dict[key]['frequency'] > 693:
    total_views_rem+=(web_page_meta_dict[key]['frequency']*web_page_meta_dict[key]['ad_slots'])



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

patterns_file_data = [x.strip() for x in patterns_file_data if len(x.strip()) > 0]


patterns = []
print("Loaded all files")

def get_ad_slot_item(index, pattern):
    # return "done"
    # import pdb; pdb.set_trace()
    # print(pattern)
    # print(index)
    tic = time.time()
    # global web_page_to_pattern_map
    
    # print(pattern,index)
    values = pattern.split('|')
    items = values[0].split(', ')#re.findall("\d+", pattern)
    items = [int(item.strip()) for item in items]
    pattern_list = items
    # coverage_support = float(values[1].strip()) 
    # cmine_metadata = items[-1]
    
    # uniqueness, coverage_support = getUniqueness(cmine_metadata, web_page_meta_dict[pattern_list[-1]]['frequency'],index,pattern)
    # del items
    # pattern_freq = 0
    # transactions_set = 
    # import pdb; pdb.set_trace()
    # for item in pattern_list: # (1,2,3) .. (2,3,4)
        # transactions_set += web_page_meta_dict[item]['transactions']
        # web_page_to_pattern[item].append(index)
        # pattern_freq = pattern_freq + web_page_meta_dict[item]['frequency']
    # print("making multiset")
    # transactions_set = functools.reduce(lambda a,b : a+b,,0)

    transactions_set = Multiset([transaction for web_page in pattern_list for transaction in web_page_meta_dict[web_page]['transactions']])
    # print("done")
    pattern_set = set(pattern_list) #106895

    # for web_page in pattern_list:
    #     pattern_dict[web_page] = True
        # web_page_to_pattern_map[web_page].append(index)

    p =  {
        'pattern': pattern_set, # {'1':true, '2':true}
        # 'pattern_freq': pattern_freq,
        # 'uniqueness': uniqueness,
        'coverage_support': len(transactions_set._elements.keys()),#coverage_support,
        'deleted':False,
        # 'uniq_users':len(transactions_set._elements.keys()),
        'users':transactions_set,
        'index':index
    }
    toc = time.time()
    print("{} : Created dict in {} seconds".format(index, toc-tic),end='\r')
    # set_patterns(p)
    return p

def get_ad_slot_item_proxy(args):
    return get_ad_slot_item(*args)
# patterns = [None]*len(patterns_file_data)

p = Pool(29)



# def set_patterns(result):
#     patterns[result['index']] = result

# print(len(patterns_file_data))
patterns = p.map(get_ad_slot_item_proxy, enumerate(patterns_file_data)) 
# get_ad_slot_item(patterns_file_data[106896],106896)

# [p.apply_async(get_ad_slot_item_proxy, (pattern,index)) for index, pattern in enumerate(patterns_file_data)]
# p.close()
# p.join()
# print(patterns)
# patterns = [get_ad_slot_item(index, pattern) for index, pattern in enumerate(patterns_file_data[:100000])]
print("got patterns")
patterns.sort(key=lambda x: x['coverage_support'], reverse=True)
print("sorted patterns")
# print((patterns[0]['uniq_users']),(patterns[-1]['uniq_users']))

web_page_to_pattern_map = defaultdict(list)

for index, pattern in enumerate(patterns):
    pattern_list = pattern['pattern']
    for web_page in pattern_list:
        web_page_to_pattern_map[web_page].append(index)

print("created index")

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


def binary_search_on_patterns(arr, x):
    ans = bisect.bisect_left(arr,x)
    if ans == len(arr):
        return None
    return ans

def linear_search_on_patterns(arr,x, skip_n=0):
    # i = 0
    ans =  None
    second_highest = None
    for index, item in enumerate(arr):
        if index < skip_n:
            continue
        if item['deleted']:
            continue
        if item['coverage_support'] >= x:
            ans = index
        elif ans is not None:
            break
        elif second_highest is None:
            second_highest = index
    return ans, second_highest


low_level_patterns = list(filter(lambda x: x['coverage_support'] < 2000,patterns))
# low_level_patterns = list(filter(lambda x: x['uniq_users'] >= 2000,patterns))
# def get_web_page_from_ad_slot(ad_slot):
#     return ad_slot.split('_')[0]

# print(patterns[:5])
# print(patterns[-5:])
# print(len(patterns))
# advertisers_data = [random.randint(220100,400100) for i in range(ADVERTISERS_DATA_LENGTH)]

advertisers_failed = []
advertisers_success = {}
web_page_to_advertiser = defaultdict(list)
views_wasted=0
s=""
cnt=0
ad_len=len(advertisers_data)
print("started allocation")
for i, advertisers_req in enumerate(advertisers_data):
    
    # global web_page_to_pattern_map
    print("looking for {}".format(advertisers_req))
    # print("Avialable Patterns:"+str(len([p  for p in patterns if p['deleted']==False] )))

    required_coverage_support = advertisers_req # requested coverage support
    
    # print(patterns[-10:])
    # import pdb; pdb.set_trace()
    # print("doing search")
    allocated_index, second_highest = linear_search_on_patterns(patterns,required_coverage_support) # Find the index of allocation
    
    allocated_value = 0

    patterns_allocated = []
    
    if allocated_index is not None:
        allocated_value = patterns[allocated_index]['uniq_users']
        cnt+=1
        patterns_allocated.append(dict(patterns[allocated_index]))

    

    # print("Requesting CS:"+str(required_coverage_support))

    if allocated_index == None: # dorakakapothae continue with next
        # import pdb; pdb.set_trace()
        if second_highest == None:
            continue
        allocated_users = set()
        allocated_users = allocated_users.union(set(patterns[second_highest]['users']))
        patterns_allocated.append(dict(patterns[second_highest]))
        # allocated_value += patterns[second_highest]['uniq_users']
        allocated_fine = False
        prev_low_level_index = -1
        while True:#second_highest is not None and required_coverage_support - len(allocated_users) < 6000:
            print("required more: {}".format(required_coverage_support - len(allocated_users)),end='\r')
            new_allocated_index, second_highest = linear_search_on_patterns(low_level_patterns,required_coverage_support - len(allocated_users), prev_low_level_index+1)
            if new_allocated_index is not None:
                prev_low_level_index = new_allocated_index
                patterns_allocated.append(dict(low_level_patterns[new_allocated_index]))
                # allocated_value += patterns[new_allocated_index]['uniq_users']
                new_users = set(low_level_patterns[new_allocated_index]['users'])
                if len(new_users - allocated_users) == 0:
                    continue
                allocated_users = allocated_users.union(new_users)
                # allocated_fine = True
                # print("{} : new allocated: {}".format(new_allocated_index, len(allocated_users) ))
                if required_coverage_support <= len(allocated_users):
                    allocated_fine = True
                    break
                continue
            if second_highest == None:
                print("none left")
                break
            prev_low_level_index = second_highest
            new_users = set(low_level_patterns[second_highest]['users'])
            if len(new_users - allocated_users) == 0:
                continue

            allocated_users = allocated_users.union(new_users)
            # allocated_value += patterns[second_highest]['uniq_users']
            patterns_allocated.append(dict(low_level_patterns[second_highest]))
            # print("{} : new allocated: {}".format(second_highest, len(allocated_users)))
        print("\n")
        if allocated_fine == False:
            print("failed to allcoate:{} {}".format(advertisers_req, len(allocated_users)))
            advertisers_failed.append(advertisers_req)
            continue
        # print(" Allocation failed:{}".format(required_coverage_support))
        allocated_value = len(allocated_users)
    print("Required: {} Min: {} Max: {} Allocate: {} allocated {} patterns ".format(required_coverage_support, patterns[-1]['uniq_users'],patterns[0]['uniq_users'], allocated_value, len(patterns_allocated)))
    # import pdb; pdb.set_trace()
    # total_views_rem-=patterns[allocated_index]['pattern_freq']
    # views_wasted+=(patterns[allocated_index]['pattern_freq']-patterns[allocated_index]['coverage_support'])
    captured_revenue += required_coverage_support # allocate ayindhi kabbati revenue penchuko
    #print(str(cnt)+"views wasted:"+str(views_wasted)+"\n")
    
    # print("{0} vadki index:{1} pattern allocate ayindhi".format(i,allocated_index))
    # print(patterns[allocated_index])
    s+=("required:"+str(required_coverage_support)+" alloc:"+str(allocated_value)+"\n")
    
    allocated_web_pages = list(set([x for pat in patterns_allocated for x in pat['pattern']]))   #list(patterns[allocated_index]['pattern']) # allocate ayina web pages list

    # patterns[allocated_index]['deleted'] = True
    # print(" ALLOCATED:"+str(patterns[allocated_index]['coverage_support'])+"  " +" ".join(patterns[allocated_index]['pattern']))
    # print(required_coverage_support,patterns[allocated_index]['coverage_support'])
    # allocated_pattern = dict(patterns[allocated_index])
    advertisers_success[i] = {}
    advertisers_success[i]['allocated_patterns'] = list(patterns_allocated)#dict(patterns[allocated_index])
    advertisers_success[i]['requirement'] = required_coverage_support
    advertisers_success[i]['allocated_adslots'] = []

    if required_coverage_support > 50000:
        print("allocated web pages:{}".format(allocated_web_pages))
    for web_page in allocated_web_pages:
        if required_coverage_support > 50000:
            print(web_page)
        allocated_ad_slot = web_page + "_" + str(web_page_meta_dict[web_page]['remaining'])
        advertisers_success[i]['allocated_adslots'].append(allocated_ad_slot)
        web_page_meta_dict[web_page]['remaining'] -= 1
        web_page_to_advertiser[web_page].append(i)
        print("Number of remaining slots in {} is {}".format(web_page,web_page_meta_dict[web_page]['remaining']))
        if web_page_meta_dict[web_page]['remaining'] == 0:
            if required_coverage_support > 50000:
                print("has 0 adslots remaining")
            removing_patterns = web_page_to_pattern_map[web_page]
            if required_coverage_support >= 0:
                print("patterns containing this webpage: {}".format(len(removing_patterns)))
            # print(removing_patterns)
            for pattern in removing_patterns:
                # if required_coverage_support > 5000:
                #     print(pattern)

                # if pattern == allocated_index:
                #     continue
                # print(len(patterns[pattern]['pattern']))
                if web_page in patterns[pattern]['pattern']:
                    # if required_coverage_support < 5000:
                    #     print("in pattern")
                    # Motham pattern ni delete cheyali antey
                    # patterns[pattern]['deleted'] = True
                    del patterns[pattern]['pattern'][web_page]
                    # if required_coverage_support < 5000:
                    #     print("deleted")
                    # patterns[pattern]['pattern_freq'] -= web_page_meta_dict[web_page]['frequency']  
                    # web_page_list = Multiset(web_page_meta_dict[web_page]['transactions'])
                    # print(pattern,web_page,len(web_page_list))
                    # if required_coverage_support < 5000:
                    #     print("listed")
                    patterns[pattern]['users'] -= Multiset(web_page_meta_dict[web_page]['transactions'])
                    # for user in web_page_meta_dict[web_page]['transactions']
                    # patterns[pattern]['users'] = Multiset([z for z in  patterns[pattern]['users'] if not z in web_page_list or web_page_list.remove(z)])
                    # if required_coverage_support < 5000:
                    #     print("new users")
                    patterns[pattern]['uniq_users'] = len(patterns[pattern]['users']._elements.keys())
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
    
    # if allocated_pattern['uniq_users'] - required_coverage_support > 1000:
    #     allocated_pattern['uniq_users'] -= required_coverage_support
    #     print("saved a new pattern of {}".format(allocated_pattern['uniq_users']))
    #     patterns.append(allocated_pattern)

    patterns.sort(key=lambda x: x['uniq_users'],reverse=True)
    web_page_to_pattern_map = defaultdict(list)
    for index, pattern in enumerate(patterns):
        pattern_list = pattern['pattern']
        for web_page in pattern_list:
            web_page_to_pattern_map[web_page].append(index)
    low_level_patterns = list(filter(lambda x: x['uniq_users'] < 2000,patterns))
    # web_page_to_advertiser[get_web_page_from_ad_slot(allocated_index)].append(i)
# PRC = captured_revenue*100.0/total_revenue

# allocated_impressions = sum([max(1.0,advertisers_success[x]['pattern_freq']/advertisers_success[x]['requirement']) for x in advertisers_success])
# AAS = allocated_impressions*10.0/len(advertisers_data)

with open(data_return_file_path,'a') as f:
    # print("heyy")
    # print(data_return_file_path)
    # views_wasted=0
    f.write(str(ad_len)+" "+str(views_wasted)+" "+str(total_views_rem)+" "+str(captured_revenue)+"\n")
    # f.write(str(AAS)+"\n")
    # print(PRC)

with open("allocs.txt",'a') as f:
    f.write(s)

print("Allocation accuracy new method: "+str(len(advertisers_success)))
print("views wasted:"+str(views_wasted))
with open(sys.argv[7],'w') as f:
    json.dump(advertisers_success,f)

with open(sys.argv[8],'w') as f:
    json.dump(web_page_to_advertiser,f)
