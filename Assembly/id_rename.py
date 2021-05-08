####
#
#   Create a new table of previous sequence names and specify the new names that NCBI accepts
#
####

# To comply with 
# https://www.ncbi.nlm.nih.gov/sites/books/NBK566986/#qkstrt_Format_Sub.how_do_i_format_a_fast
# to run from  inside python3:
# exec(open('id_rename.py').read())
# then:

import re
filename = 'ids_original.txt'

new_lines = []

counter = 0

new_name_template_1 = 'SEQ' 
new_name_template_2 = '[organism=Awesome species] [sample=xyz] '

with open(filename) as sequence_ids:
	for sequence in sequence_ids:
		new_name = sequence.split('\n')[0] + '\t' + new_name_template_1 + str(counter) + ' ' + new_name_template_2
		# note in the description if this was placed by ragtag
		if re.search(r'N*_Rag', sequence) is None:
			new_name = new_name + 'unplaced genomic scaffold WGS\n'
		else:
			new_name = new_name + 'mapped to ' + sequence.split('_Rag')[0] + ' in REF_accession\n'
		new_lines.append(new_name)
		counter += 1

new_file = open('ids_new.txt','w')
new_file.writelines(new_lines)
new_file.close()


