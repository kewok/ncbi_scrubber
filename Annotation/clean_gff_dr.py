####
#
# purge features flagged in the discrepency report by locus tag from your annotation file.
# 
####

import csv
import sys
import re

bad_features = open('bad_loci.txt','r+')
bf = bad_features.readlines()

# A very unpythonic solution
bad_features=[]

for bad in bf:
	bad_features.append(bad.split('\n')[0])

original_gff = open('old.gff','r+') # The original gff file
gffs = original_gff.readlines()

keeper_lines = []
k = 0
for feature in gffs:
	k = k+1
	print(k)
	if ('locus_tag' + feature.split('locus_tag')[1].split(';')[0]) not in bad_features:
		keeper_lines.append(feature)

with open('cleaned.gff','w') as f:
	f.writelines(keeper_lines)


