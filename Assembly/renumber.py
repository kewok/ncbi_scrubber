import csv
import re
import sys

f = open(sys.argv[1],'r+') # Input sequences that need removing
lines = f.readlines()

# re-number the sequences
new_names = []

k = 0
for name in temp_new_names:
	keep = name.split('[org')[1]
	new_names.append('SEQ' + str(k) + ' [org' + keep)
	k += 1

