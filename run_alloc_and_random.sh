#!/bin/bash

for i in {5..20..5}
do
    echo "ALLOCATING WITH OUR NEW METHOD: $i"
    python allocation.py ../test1/dataset_bms_pos.txt_0.065_0.0_0.6_output.txt ../adslot/web_page_meta_dict.json ../adslot/web_page_freq_sorted.pkl $i
    echo "AD REPEATABILITY OF OUR NEW METHOD : $i"
    python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./new_alloc_web_page_to_adv.json 
    echo "ALLOCATING WITH RANDOM METHOD: $i"
    python random_allocation.py ../adslot/web_page_meta_dict.json $i
    echo "AD REPEATABILITY OF RANDOM METHOD: $i"
    python ad_repeatability_random_alloc.py ../test1/dataset_bms_pos.txt ./random_alloc_web_page_to_adv.json 
done