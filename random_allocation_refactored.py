import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict


META_DATA_FILE_PATH = sys.argv[2]
print("META_DATA_FILE_PATH", META_DATA_FILE_PATH)
data_return_file_path = sys.argv[5]
with open(META_DATA_FILE_PATH,'r') as f:
    web_page_meta_dict = json.load(f)
DATA_FILE_PATH = sys.argv[7]
data_file = open(DATA_FILE_PATH,'r')
web_page_meta_dict2 = dict(web_page_meta_dict)

total_views_rem=0
for key in web_page_meta_dict:
    total_views_rem+=(web_page_meta_dict[key]['frequency']*web_page_meta_dict[key]['ad_slots'])

web_page_meta_dict = web_page_meta_dict2
webpage_user_dict = {}


advertisers_data = map(int,sys.argv[4].split(','))
advertisers_data.sort(reverse=True)
ADVERTISERS_DATA_LENGTH = len(advertisers_data)
advertisers_failed = []
advertisers_success = defaultdict(list)
advertisers_freq_req = [0]*ADVERTISERS_DATA_LENGTH
WEB_PAGES_COUNT = len(web_page_meta_dict)

allocated_lookup = set()
captured_revenue = 0
total_revenue = sum(advertisers_data)
web_page_to_advertiser = defaultdict(list)
i = 0
no_of_allocated = 0
views_wasted=0
curtotal_views=0
sum_of_scaled_allocated_impressions = 0
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
            if cur_web_page not in deleted_web_pages:
                deleted_web_pages[cur_web_page] = dict(web_page_meta_dict[cur_web_page])
            deleted_web_pages[cur_web_page]['ad_slots'] += 1
            del web_page_meta_dict[cur_web_page]
    if len(current_allocation) < required_coverage_support:
        final_failed.append({'req':required_coverage_support,'i':i})
        # you can also remove this because the earlier while loop only exits after perfect allocation or no more pages left.
        web_page_meta_dict.update(deleted_web_pages)
        # print("ReAllocation failed for {} , got only {}".format(required_coverage_support, len(current_allocation)))
        continue
    captured_revenue += required_coverage_support
    no_of_allocated += 1

print(data_return_file_path)
with open(data_return_file_path,'a') as f:
    f.write(str(ADVERTISERS_DATA_LENGTH)+" "+str(views_wasted)+" "+str(total_views_rem)+" "+str(captured_revenue)+"\n")

print("Allocation accuracy: "+str(no_of_allocated))
print("total views sold: "+ str(captured_revenue))
with open(sys.argv[8],'w') as f:
    json.dump(advertisers_success,f)

with open(sys.argv[9],'w') as f:
    json.dump(web_page_to_advertiser,f)
