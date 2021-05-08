####
#
#   Generate a bed file from a list of unacceptable sequences regions so that you can replace sequences NCBI rejects with 'X'
#
####

import csv
import sys
import re

trim_file = open(sys.argv[1],'r+') # Input segments that need to be masked in bad.bed for bedtools
lines = trim_file.readlines()

seqName = []
seqRegion_Start = []
seqRegion_End = []

def add_entry(name_vector, start_vector, end_vector, name, region):
	name_vector.append(name)
	region_range = region.split('..')
	start_vector.append(int(region_range[0]) - 1) # Note bedtools uses zero indexing, so correct accordingly for start value; 
	end_vector.append(int(region_range[1])) # however, because bedtools does it exclusive of the last value, you want to make sure the last value identified by ncbi is marked out as well as ncbi does it start..end (https://www.ncbi.nlm.nih.gov/genbank/samplerecord/)

for line in lines:
	if re.search('SEQ', line) is not None:
		span = line.split('\t')[2]
		seq_name = line.split('\t')[0]
		# If there are multiple regions in the contig
		if re.search(',',span):
			newRegions = span.split(',')
			for region in newRegions:
				add_entry(seqName, seqRegion_Start, seqRegion_End, seq_name, region)
		else:
			add_entry(seqName, seqRegion_Start, seqRegion_End, seq_name, span)

with open('bad.bed','w') as f:
	writer = csv.writer(f, delimiter='\t', lineterminator='\n')	
	writer.writerows(zip(seqName, seqRegion_Start, seqRegion_End))

#csv_dict = csv.DictReader(trim_data, delimiter=",",quotechar="\"")
