#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

transaction_amount_array = []
candidate_ids = set()

for row in csv.reader(fileinput.input(), delimiter='|'):
	transaction_amount_array.append(float(row[14]))
	candidate_ids.add(row[16])

def get_mean(array1):
	return sum(array1) / len(array1)
	
def get_median(array1):
	median = 0
	array1.sort()
	if len(array1) % 2 == 1:
		median_index = (len(array1) - 1) / 2
		median = array1[median_index]
	else:
		median_index_1 = (len(array1)) / 2
		median_index_2 = median_index_1 + 1
		median_1 = array1[median_index_1]
		median_2 = array1[median_index_2]
		median = (median_1 + median_2) / 2
	return median

def get_stdev(array1, mean):
	num = [ (array1[i] - mean) ** 2 for i in range(len(array1)) ]
	return ( sum(num) / len(array1) ) ** 0.5

def get_candidate_ids(set1):
	str1 = ""
	while(len(set1) > 0):
		str1 += set1.pop() + ', '
	return str1

total = sum(transaction_amount_array)
minimum = min(transaction_amount_array)
maximum = max(transaction_amount_array)
mean = get_mean(transaction_amount_array)
median = get_median(transaction_amount_array)
stdev = get_stdev(transaction_amount_array, mean)

##### Print out the stats
print "Total: %s" % total
print "Minimum: %s" % minimum
print "Maximum: %s" % maximum
print "Mean: %s" % mean
print "Median: %s" % median
# square root can be calculated with N**0.5
print "Standard Deviation: %s" % stdev

##### Comma separated list of unique candidate ID numbers
print "Candidates: %s" % get_candidate_ids(candidate_ids)

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""

    norm = (value - minimum) / (maximum - minimum)

    return norm

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
