####
#
# tbl2asn_gff typically exhibits a slew of fatal error features from your GFF file. This code creates a CSV file, called bad_loci.txt that will identify the locus_tags that need to be revised or removed from the original GFF file
#
####

import csv
import sys
import re

trim_file = open(sys.argv[1],'r+') # Input features that were identified as naughty
lines = trim_file.readlines()

# Note using set permits you to avoid duplicates:
bad_loci = set()

for line in lines:
	bad_loci.add(line.split('\t')[3].split('\n')[0])

with open('bad_loci.txt','w') as f:
	for bad_locus in bad_loci:
		f.write('locus_tag=' + str(bad_locus) + '\n')


