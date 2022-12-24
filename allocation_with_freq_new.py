import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict, Counter
from multiprocessing import Process, Manager, Pool
import glob


print("Allocation with freq")
print(sys.argv)

PATTERNS_FOLDER_PATH = sys.argv[1]
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


    

# print("total_pages: {}".format(len(web_page_meta_dict.keys())))
# print("low_rf_pages: {}".format(len(web_page_low_rf_dict.keys())))
with open(FREQ_SORT_DATA_FILE_PATH,'r') as f:
    web_page_freq_sorted = pickle.load(f)

patterns_file_list = glob.glob("{}/*.txt".format(PATTERNS_FOLDER_PATH))

print(patterns_file_list)

patterns_file_data = []

for patterns_file in patterns_file_list:
    # with open(PATTERNS_FOLDER_PATH) as f:
    patterns_file_data += open(patterns_file).read().splitlines()

total_views_rem=0
for key in web_page_meta_dict:
    # if web_page_meta_dict[key]['frequency'] > 693:
    total_views_rem+=(web_page_meta_dict[key]['frequency']*web_page_meta_dict[key]['ad_slots'])

# patterns_file_data = [x.strip() for x in patterns_file_data]

web_page_to_pattern_map = defaultdict(list)
patterns = {}
print("Loaded all files")

def get_ad_slot_item(pattern, index):
    data = pattern.split('|')
    pattern_list = data[0].strip().split(',')#re.findall("\d+", pattern)
    pattern_list = [p.strip() for p in pattern_list]
    # pattern_freq = 0
    transactions_set = Counter()
    for item in pattern_list: # (1,2,3) .. (2,3,4)
        transactions_set.update(web_page_meta_dict[item]['transactions'])
        # pattern_freq = pattern_freq + web_page_meta_dict[item]['frequency']
    cur_patterns = set()
    for web_page in pattern_list:
        # pattern_dict[web_page] = True
        cur_patterns.add(web_page)
        web_page_to_pattern_map[web_page].append(index)

    return {
        'pattern': cur_patterns, # {'1':true, '2':true}
        # 'pattern_freq': pattern_freq,
        # 'uniqueness': uniqueness,
        # 'coverage_support': float(data[1].strip()),
        # 'deleted':False,
        # 'uniq_users':len(transactions_set),
        'users':transactions_set
    }


def yield_args(patterns_file_data, patterns):
    for index, pattern in enumerate(patterns_file_data):
        yield pattern, index, patterns

def get_ad_slot_item_proxy(args):
    return get_ad_slot_item(*args)

for index, pattern in enumerate(patterns_file_data):
    patterns[index] = get_ad_slot_item(pattern, index)
print("got patterns")

for web_page in web_page_meta_dict.keys():
    web_page_meta_dict[web_page]['remaining'] = web_page_meta_dict[web_page]['ad_slots'] 
    if web_page not in web_page_to_pattern_map:
        web_page_low_rf_dict[web_page] = dict(web_page_meta_dict[web_page])
        del web_page_meta_dict[web_page]

print("total_pages: {}".format(len(web_page_meta_dict)))
print("low_rf_pages: {}".format(len(web_page_low_rf_dict)))        

def linear_search_on_patterns(patterns,x):
    second_best = None
    for key in patterns:
        if abs(len(patterns[key]['users'])-x) <= 0.1*x: #len(patterns[key]['users']) >= x and len(patterns[key]['users']) <= 1.2*x:
            return key
        # elif second_best is None:
            # second_best = key
        # elif len(patterns[key]['users']) >= x:
        #     if len(patterns[key]['users']) < len(patterns[second_best]['users']) or len(patterns[second_best]['users']) < x :
        #         second_best = key
        elif second_best is None or abs(len(patterns[key]['users']) - x) < abs(len(patterns[second_best]['users']) - x):
            # if second_best is None or len(patterns[second_best]['users']) <= len(patterns[key]['users']):
            second_best = key
    return second_best


advertisers_failed = []
advertisers_success = {}
web_page_to_advertiser = defaultdict(list)
views_wasted=0
s=""
cnt=0
ad_len=len(advertisers_data)
for i, advertisers_req in enumerate(advertisers_data):
    print("current advertiser: {}".format(i))
    print("total_pages: {}".format(len(web_page_meta_dict)))
    print("low_rf_pages: {}".format(len(web_page_low_rf_dict)))
    print("total patterns: {}".format(len(patterns)))
    # advertisers_failed.append({'req':advertisers_req,'i':i})
    # continue
    
    required_coverage_support = advertisers_req # requested coverage support
    
    allocated_index = linear_search_on_patterns(patterns, required_coverage_support)

    clean_allocation = False
    if allocated_index == None or len(patterns[allocated_index]['users']) >= required_coverage_support:
        clean_allocation = True

    current_allocation = {}
    if clean_allocation == False:
        print("clean alloc failed")
        if allocated_index == None:
            # current_allocation['uniq_users'] = 0
            current_allocation['users'] = Counter()
            current_allocation['pattern'] = set()
        else:
            print("allocated: {} required: {}".format(len(patterns[allocated_index]['users']),required_coverage_support))
            current_allocation = dict(patterns[allocated_index])
        current_allocation['allocated_adslots'] = []
        deleted_web_pages = {}
        while len(current_allocation['users']) < required_coverage_support and len(web_page_low_rf_dict) > 0:
            cur_low_rf_web_page = random.choice(web_page_low_rf_dict.keys())
            allocated_adslot = cur_low_rf_web_page + "_" + str(web_page_low_rf_dict[cur_low_rf_web_page]['remaining'])
            current_allocation['allocated_adslots'].append(allocated_adslot)
            current_allocation['users'] += Counter(web_page_low_rf_dict[cur_low_rf_web_page]['transactions'])
            # current_allocation['uniq_users'] = len(set(current_allocation['users']))
            # current_allocation['pattern_freq'] += web_page_meta_dict[cur_low_rf_web_page]['frequency']
            web_page_low_rf_dict[cur_low_rf_web_page]['remaining'] -= 1
            # print("alloc {}".format(cur_low_rf_web_page))
            if web_page_low_rf_dict[cur_low_rf_web_page]['remaining'] == 0:
                # import pdb; pdb.set_trace()
                if cur_low_rf_web_page not in deleted_web_pages:
                    deleted_web_pages[cur_low_rf_web_page] = dict(web_page_low_rf_dict[cur_low_rf_web_page])
                deleted_web_pages[cur_low_rf_web_page]['remaining'] += 1 
                del web_page_low_rf_dict[cur_low_rf_web_page]
                # print("deleting {} current: {} required: {}".format(cur_low_rf_web_page,current_allocation['uniq_users'], required_coverage_support ))
        
        if len(current_allocation['users']) < required_coverage_support:
            advertisers_failed.append({'req':advertisers_req,'i':i})
            web_page_low_rf_dict.update(deleted_web_pages)
            print("Allocation failed for {} , got only {}".format(required_coverage_support, len(current_allocation['users'])))
            print("remaining low_rf_pages: {}".format(len(web_page_low_rf_dict)))
            continue

    if clean_allocation == False:
        advertisers_success[i] = dict(current_allocation)
        advertisers_success[i]['pattern'] = list(advertisers_success[i]['pattern'])
    else:
        advertisers_success[i] = dict(patterns[allocated_index])
        advertisers_success[i]['allocated_adslots'] = []
        advertisers_success[i]['pattern'] = list(advertisers_success[i]['pattern'])
    advertisers_success[i]['requirement'] = required_coverage_support


    # total_views_rem-=advertisers_success[i]['pattern_freq']
    # views_wasted+=(patterns[allocated_index]['pattern_freq']-patterns[allocated_index]['coverage_support'])
    captured_revenue += required_coverage_support # allocate ayindhi kabbati revenue penchuko

    if allocated_index == None: # web pages delete chesey pani ledu kabbati continue
        continue

    allocated_web_pages = list(patterns[allocated_index]['pattern']) # allocate ayina web pages list

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
                if web_page in patterns[pattern]['pattern']:
                    patterns[pattern]['pattern'].remove(web_page)
                    if len(patterns[pattern]['pattern']) == 0:
                        # patterns[pattern]['deleted'] = True
                        del patterns[pattern]
                        continue
                    # patterns[pattern]['pattern_freq'] -= web_page_meta_dict[web_page]['frequency']  
                    # web_page_list = list(web_page_meta_dict[web_page]['transactions'])
                    patterns[pattern]['users'] -= Counter(web_page_meta_dict[web_page]['transactions']) #[z for z in  patterns[pattern]['users'] if not z in web_page_list or web_page_list.remove(z)] 
                    # patterns[pattern]['uniq_users'] = len(set(patterns[pattern]['users']))
                else:
                    # import pdb; pdb.set_trace()
                    print("ERRRORR")
                    print(web_page)
                    print(patterns[pattern]['pattern'])
            web_page_to_pattern_map[web_page] = []
            # del web_page_to_pattern_map[web_page]
            del web_page_meta_dict[web_page]

# allocated_impressions = sum([max(1.0,advertisers_success[x]['pattern_freq']/advertisers_success[x]['requirement']) for x in advertisers_success])
# AAS = allocated_impressions*10.0/len(advertisers_data)

web_page_meta_dict.update(web_page_low_rf_dict)
final_failed = []

for failed in advertisers_failed:
    print("reallocating  {}".format(failed))
    print("remaining web pages: {}".format(len(web_page_meta_dict)))
    current_allocation = set()
    allocated_adslots = []
    deleted_web_pages = {}
    while len(current_allocation) < failed['req'] and len(web_page_meta_dict) > 0:
        i = failed['i']
        cur_web_page = random.choice(web_page_meta_dict.keys())
        allocated_ad_slot = cur_web_page + "_" + str(web_page_meta_dict[cur_web_page]['remaining'])
        allocated_adslots.append(allocated_ad_slot)
        current_allocation=current_allocation.union(web_page_meta_dict[cur_web_page]['transactions'])
        web_page_to_advertiser[cur_web_page].append(i)
        web_page_meta_dict[cur_web_page]['remaining'] -= 1
        if web_page_meta_dict[cur_web_page]['remaining'] == 0:
            if cur_web_page not in deleted_web_pages:
                deleted_web_pages[cur_web_page] = dict(web_page_meta_dict[cur_web_page])
            deleted_web_pages[cur_web_page]['remaining'] += 1
            del web_page_meta_dict[cur_web_page]
    if len(current_allocation) < failed['req']:
        final_failed.append({'req':advertisers_req,'i':i})
        web_page_meta_dict.update(deleted_web_pages)
        print("ReAllocation failed for {} , got only {}".format(failed['req'], len(current_allocation)))
        continue
    
    # advertisers_success[i]['allocated_adslots'].append(allocated_ad_slot)


# for i, advertisers_req in enumerate(advertisers_failed):


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
