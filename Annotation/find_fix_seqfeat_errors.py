####
#
# purge features flagged in the validation file from your annotation 
# 
####

import csv
import sys
import re

val_file=open('My_validation_File.val','r+',encoding='latin-1')
bf=val_file.readlines()

original_gff = open('old.gff','r+') # The original gff file
gffs = original_gff.readlines()

# Get the Sequin ids for the entries that are naughty
bad_ids = []
bad_names = []
for line in bf:
	if 'SEQ_INST.StopInProtein' in line:
		bad_ids.append(int(re.search(r"\<(\d+)\>", line)[1]))
		bad_names.append(line.split('(')[1].split(' - ')[0]) # since it's always of the form STUFF (product_name - MORE STUFF

# match the Sequin names with locus tags in the gff file
bad_loci = []
for i in range(0, len(gffs)):
	if 'Name=' in gffs[i]:
		gene_name = gffs[i].split('Name=')[1].split(';')[0]
		print(i)
		if gene_name in bad_names:
			bad_loci.append(gffs[i].split('locus_tag=')[1].split(';')[0])

keeper_lines = []
k = 0
for feature in gffs:
	k = k+1
	print(k)
	if (feature.split('locus_tag=')[1].split(';')[0]) not in bad_loci:
		keeper_lines.append(feature)

with open('cleaner.gff','w') as f:
	f.writelines(keeper_lines)


