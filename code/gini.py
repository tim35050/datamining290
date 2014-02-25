#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
from collections import defaultdict
from collections import Counter 

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

OBAMA_ID = 'P80003338'
ROMNEY_ID = 'P80003353'

CANDIDATES = {
    OBAMA_ID: 'Obama',
    ROMNEY_ID: 'Romney',
}

############### Set up variables
all_contributed_candidate_ids = []
zip_contributed_candidate_ids = defaultdict(list)
zip_count = defaultdict(int)

############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    all_contributed_candidate_ids.append(candidate_id)
    zip_code = row[ZIP_CODE]
    zip_contributed_candidate_ids[zip_code].append(candidate_id)
    zip_count[zip_code] += 1

def get_overall_gini_index(contributed_candidate_ids):
    candidate_counter = Counter()
    candidate_counter.update(contributed_candidate_ids)
    candidate_counts = list(candidate_counter.values())
    return calculate_gini(candidate_counts)

def get_weighted_gini_index(zip_contributed_candidate_ids, zip_count):
    zip_candidate_counts = {}
    total_count = sum(list(zip_count.values()))
    weighed_ginis = []
    for zip_code in zip_contributed_candidate_ids:
        candidate_counter = Counter()
        candidate_counter.update(zip_contributed_candidate_ids[zip_code])
        candidate_counts = list(candidate_counter.values())
        gini = calculate_gini(candidate_counts)
        fraction = zip_count[zip_code] / float(total_count)
        weighed_ginis.append(gini * fraction)
    return sum(weighed_ginis)

def calculate_gini(counts):
    gini_sum = 0
    squared_fracs = []
    total = sum(counts)
    for count in counts:
        squared_fracs.append((count/float(total))**2)
    return 1 - sum(squared_fracs)

###
# TODO: calculate the values below:
gini = get_overall_gini_index(all_contributed_candidate_ids)  # current Gini Index using candidate name as the class
split_gini = get_weighted_gini_index(zip_contributed_candidate_ids, zip_count)  # weighted average of the Gini Indexes using candidate names, split up by zip code
##/

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
