####
#
#   Rematch the sequence ids. This differs from rematch_ids.py in assuming old sequences are of the form new_sequence_id
#
####


import csv
import re
import sys

f = open(sys.argv[1],'r+') # Original input sequence names
lines = f.readlines()

old_names = []
temp_new_names = []

for line in lines:
	if re.search('SEQ', line) is not None:
		old_names.append(line.split(' ')[0])
		temp_new_names.append(line.split('\n')[0])

# Now identify the previous value that corresponds to the new sequence value and rename SEQ... accordingly

new_seqs = open(sys.argv[2],'r+') # new sequence names
lines = new_seqs.readlines()

previous_name = []
new_names = []

k = 0
for line in lines:
	value = line.split('\n')[0]
	previous_name.append(value)
	entry = old_names.index(value)
	new_name = temp_new_names[entry].split('[org')[1]
	new_name = 'SEQ' + str(k) + ' [org' + new_name
	k += 1
	new_names.append(new_name)
	print(str(k) + 'th sequence id processed')

with open('revised_name_table.txt','w') as f:
	writer = csv.writer(f, delimiter='\t', lineterminator='\n')	
	writer.writerows(zip(previous_name, new_names))
