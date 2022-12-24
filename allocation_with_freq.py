import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict

# cat *_level_patterns.txt > patterns.txt
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
min_rf = int(sys.argv[9])

print("meta data file path:{}".format(META_DATA_FILE_PATH))

print("got min rf : {}".format(min_rf))

with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)

web_page_low_rf_dict  = {}

for web_page in web_page_meta_dict:
    if web_page_meta_dict[web_page]['frequency'] < min_rf :
        web_page_low_rf_dict[web_page] = dict(web_page_meta_dict[web_page])
        # del web_page_meta_dict[key]
    web_page_meta_dict[web_page]['remaining'] = web_page_meta_dict[web_page]['ad_slots'] 

print("total_pages: {}".format(len(web_page_meta_dict.keys())))
print("low_rf_pages: {}".format(len(web_page_low_rf_dict.keys())))
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

patterns_file_data = [x.strip() for x in patterns_file_data]

web_page_to_pattern_map = defaultdict(list)
patterns = []
print("Loaded all files")

def get_ad_slot_item(pattern, index):
    # global web_page_to_pattern_map
    
    # # print(pattern,index)
    # items = re.findall("\d+", pattern)
    # pattern_list = items[:-1]
    # cmine_metadata = items[-1]
    values = pattern.split('|')
    items = values[0].split(', ')#re.findall("\d+", pattern)
    items = [int(item.strip()) for item in items]
    pattern_list = items
    coverage_support = float(values[1].strip())
    
    # uniqueness, coverage_support = getUniqueness(cmine_metadata, web_page_meta_dict[pattern_list[-1]]['frequency'],index,pattern)
    del items
    pattern_freq = 0
    transactions_set = list()
    # import pdb; pdb.set_trace()
    for item in pattern_list: # (1,2,3) .. (2,3,4)
        transactions_set += web_page_meta_dict[item]['transactions']
    #     # web_page_to_pattern[item].append(index)
    #     pattern_freq = pattern_freq + web_page_meta_dict[item]['frequency']
    

    pattern_dict = {}

    for web_page in pattern_list:
        pattern_dict[web_page] = True
        # web_page_to_pattern_map[web_page].append(index)

    return {
        'pattern': pattern_dict, # {'1':true, '2':true}
        # 'pattern_freq': pattern_freq,
        # 'uniqueness': uniqueness,
        'coverage_support': coverage_support,
        'deleted':False,
        'uniq_users':len(set(transactions_set)),
        'users':transactions_set
    }



patterns = [get_ad_slot_item(pattern, index) for index, pattern in enumerate(patterns_file_data)]
print("got patterns")
patterns.sort(key=lambda x: x['uniq_users'], reverse=True)

# print((patterns[0]['uniq_users']),(patterns[-1]['uniq_users']))


for index, pattern in enumerate(patterns):
    pattern_list = pattern['pattern']
    for web_page in pattern_list:
        web_page_to_pattern_map[web_page].append(index)



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

def linear_search_on_patterns(arr,x):
    # i = 0
    ans =  None
    for index, item in enumerate(arr):
        if item['deleted']:
            continue
        if item['uniq_users'] >= x:
            ans = index
        elif ans is not None:
            return ans, True
        else:
            return index, False
    return ans, ans!=None

# def get_web_page_from_ad_slot(ad_slot):
#     return ad_slot.split('_')[0]

# print(patterns[:5])
# print(patterns[-5:])
# print(len(patterns))
# advertisers_data = [random.randint(220100,400100) for i in range(ADVERTISERS_DATA_LENGTH)]

# print([x['pattern'] for x in patterns[:5]])
# print(web_page_to_pattern_map['11'])
# print(web_page_to_pattern_map['11'])

advertisers_failed = []
advertisers_success = {}
web_page_to_advertiser = defaultdict(list)
views_wasted=0
s=""
cnt=0
ad_len=len(advertisers_data)
for i, advertisers_req in enumerate(advertisers_data):
    # global web_page_to_pattern_map
    # print("Avialable Patterns:"+str(len([p  for p in patterns if p['deleted']==False] )))
    print("total_pages: {}".format(len(web_page_meta_dict.keys())))
    print("low_rf_pages: {}".format(len(web_page_low_rf_dict.keys())))
    
    required_coverage_support = advertisers_req # requested coverage support
    
    # print(patterns[-10:])
    # import pdb; pdb.set_trace()
    allocated_index, clean_allocation = linear_search_on_patterns(patterns,required_coverage_support) # Find the index of allocation
    
    # allocated_value = None
    current_allocation = {}
    if clean_allocation == False:
        print("clean alloc failed")
        if allocated_index == None:
            current_allocation['uniq_users'] = 0
            current_allocation['users'] = []
            current_allocation['pattern_freq'] = 0
        else:
            
            print("allocated: {} required: {}".format(patterns[allocated_index]['uniq_users'],required_coverage_support))
            current_allocation = dict(patterns[allocated_index])
        current_allocation['allocated_adslots'] = []
        while current_allocation['uniq_users'] < required_coverage_support and len(web_page_low_rf_dict.keys()) > 0:
            cur_low_rf_web_page = random.choice(web_page_low_rf_dict.keys())
            allocated_adslot = cur_low_rf_web_page + "_" + str(web_page_meta_dict[cur_low_rf_web_page]['remaining'])
            current_allocation['allocated_adslots'].append(allocated_adslot)
            current_allocation['users'] += web_page_low_rf_dict[cur_low_rf_web_page]['transactions']
            current_allocation['uniq_users'] = len(set(current_allocation['users']))
            current_allocation['pattern_freq'] += web_page_meta_dict[cur_low_rf_web_page]['frequency']
            web_page_meta_dict[cur_low_rf_web_page]['remaining'] -= 1
            # print("alloc {}".format(cur_low_rf_web_page))
            if web_page_meta_dict[cur_low_rf_web_page]['remaining'] == 0:
                # import pdb; pdb.set_trace()
                del web_page_low_rf_dict[cur_low_rf_web_page]
                # print("deleting {} current: {} required: {}".format(cur_low_rf_web_page,current_allocation['uniq_users'], required_coverage_support ))
        
        if current_allocation['uniq_users'] < required_coverage_support:
            advertisers_failed.append(advertisers_req)
            continue
        # if current_allocation['uniq_users'] >= required_coverage_support:
        #     captured_revenue += required_coverage_support
        #     advertisers_success[i] = dict(patterns[allocated_index])
        #     advertisers_success[i]['requirement'] = required_coverage_support
        #     advertisers_success[i]['allocated_adslots'] = []

    # if clean_allocation == False and allocated_index is None:
    #     advertisers_failed.append(advertisers_req)
    #     continue
    if clean_allocation == False:
        advertisers_success[i] = dict(current_allocation)
    else:
        advertisers_success[i] = dict(patterns[allocated_index])
        advertisers_success[i]['allocated_adslots'] = []
    advertisers_success[i]['requirement'] = required_coverage_support


    total_views_rem-=advertisers_success[i]['pattern_freq']
    # views_wasted+=(patterns[allocated_index]['pattern_freq']-patterns[allocated_index]['coverage_support'])
    captured_revenue += required_coverage_support # allocate ayindhi kabbati revenue penchuko

    if allocated_index == None: # web pages delete chesey pani ledu kabbati continue
        continue

    

    # if allocated_index is not None:
        # allocated_value = patterns[allocated_index]['uniq_users']
        # cnt+=1

    # print("Required: {} Min: {} Max: {} Allocate: {}".format(required_coverage_support, patterns[-1]['pattern_freq'],patterns[0]['pattern_freq'], allocated_value))

    # print("Requesting CS:"+str(required_coverage_support))

    # if allocated_index == None: # dorakakapothae continue with next
        # advertisers_failed.append(advertisers_req)
        # print(" Allocation failed:{}".format(required_coverage_support))
        # continue
    # import pdb; pdb.set_trace()
    #print(str(cnt)+"views wasted:"+str(views_wasted)+"\n")
    
    # print("{0} vadki index:{1} pattern allocate ayindhi".format(i,allocated_index))
    # print(patterns[allocated_index])
    # s+=("required:"+str(required_coverage_support)+" alloc:"+str(patterns[allocated_index]['coverage_support'])+"\n")
    # import pdb; pdb.set_trace()
    allocated_web_pages = list(patterns[allocated_index]['pattern']) # allocate ayina web pages list

    # patterns[allocated_index]['deleted'] = True
    # print(" ALLOCATED:"+str(patterns[allocated_index]['coverage_support'])+"  " +" ".join(patterns[allocated_index]['pattern']))
    # print(required_coverage_support,patterns[allocated_index]['coverage_support'])
    

    for web_page in allocated_web_pages:
        
        allocated_ad_slot = web_page + "_" + str(web_page_meta_dict[web_page]['remaining'])
        advertisers_success[i]['allocated_adslots'].append(allocated_ad_slot)
        web_page_meta_dict[web_page]['remaining'] -= 1
        web_page_to_advertiser[web_page].append(i)
        # print("Number of remaining slots in {} is {}".format(web_page,web_page_meta_dict[web_page]['remaining']))
        if web_page_meta_dict[web_page]['remaining'] == 0:
            print("deleting {}".format(web_page))
            removing_patterns = web_page_to_pattern_map[web_page]
            for pattern in removing_patterns:
                if pattern <= 10:
                    print("allocated_index: {} pattern : {}".format(allocated_index, pattern))
                    print(patterns[pattern]['pattern'])
                # if pattern == allocated_index:
                #     continue
                if web_page in patterns[pattern]['pattern']:

                    # Motham pattern ni delete cheyali antey
                    # patterns[pattern]['deleted'] = True
                    del patterns[pattern]['pattern'][web_page]
                    if len(patterns[pattern]['pattern'].keys()) == 0:
                        patterns[pattern]['deleted'] = True
                        continue
                    patterns[pattern]['pattern_freq'] -= web_page_meta_dict[web_page]['frequency']  
                    web_page_list = list(web_page_meta_dict[web_page]['transactions'])
                    patterns[pattern]['users'] = [z for z in  patterns[pattern]['users'] if not z in web_page_list or web_page_list.remove(z)] 
                    patterns[pattern]['uniq_users'] = len(set(patterns[pattern]['users']))
                else:
                    # import pdb; pdb.set_trace()
                    print("ERRRORR")
                    print(web_page)
                    print(patterns[pattern]['pattern'])
            web_page_to_pattern_map[web_page] = []
            del web_page_meta_dict[web_page]

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
    
    patterns.sort(key=lambda x: x['uniq_users'],reverse=True)
    web_page_to_pattern_map = defaultdict(list)
    for index, pattern in enumerate(patterns):
        pattern_list = pattern['pattern']
        for web_page in pattern_list:
            web_page_to_pattern_map[web_page].append(index)
    # web_page_to_advertiser[get_web_page_from_ad_slot(allocated_index)].append(i)
# PRC = captured_revenue*100.0/total_revenue

allocated_impressions = sum([max(1.0,advertisers_success[x]['pattern_freq']/advertisers_success[x]['requirement']) for x in advertisers_success])
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
