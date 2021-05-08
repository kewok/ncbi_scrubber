####
#
#   Generate a list of completely unacceptable sequences
#
####


import csv
import sys
import re

trim_file = open(sys.argv[1],'r+') # Input sequences that need removing
lines = trim_file.readlines()

seqName = []

for line in lines:
	if re.search('SEQ', line) is not None:
		seq_name = line.split('\t')[0]
		seqName.append(seq_name)

with open('contaminant_sequences.txt','w') as f:
	for line in seqName:
		f.write(line + '\n')

