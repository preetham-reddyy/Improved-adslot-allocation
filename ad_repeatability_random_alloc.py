import os
import sys
import pickle
import json
import re
import bisect
import itertools
import random
from collections import defaultdict

# transactional data
USER_DATA = sys.argv[1]

WEB_PAGE_TO_ADV_FILE_PATH  = sys.argv[2]

# print("WEB_PAGE_TO_ADV_FILE_PATH", WEB_PAGE_TO_ADV_FILE_PATH)

with open(WEB_PAGE_TO_ADV_FILE_PATH,'r') as f:
    web_page_to_advertiser = json.load(f)

def initial_count():
    return -1


user_file = open(USER_DATA,'r')
i = 0
repeated_list = list()
for user_data in user_file:
    i += 1
    # print(user_data)
    web_pages = user_data.strip().split(',')
    repeated_dict = defaultdict(initial_count)
    # print(web_pages)
    for web_page in web_pages:
        # print("web_page", web_page)
        if web_page not in web_page_to_advertiser:
            continue
        # print("web_page", web_page)
        for adv in web_page_to_advertiser[web_page]:
            repeated_dict[adv] += 1
    repeated_count = 0
    for key in repeated_dict:
        # if repeated_dict[key] > 0:
        repeated_count += repeated_dict[key]
    repeated_list.append(repeated_count)

# print(repeated_list)
# print(sum(repeated_list))
# print(len(web_page_to_advertiser))
print(sum(repeated_list)*1.0/i)
