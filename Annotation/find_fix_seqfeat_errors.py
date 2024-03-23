####
#
# purge features flagged in the validation file from your annotation 
# 
####

import csv
import sys
import re

accession_prefix = 'my_accessio_prefix' # https://www.ncbi.nlm.nih.gov/genbank/acc_prefix/
gene_name_prefix =  'gen_prefix|' # usually in the form X1X| 

val_file=open('My_validation_File.val','r+',encoding='latin-1')
bf=val_file.readlines()

original_gff = open('old.gff','r+') # The original gff file
gffs = original_gff.readlines()

# Get the Sequin ids for the entries that are naughty
bad_contigs = []
bad_names = []
bad_start = []
bad_end = []
for line in bf:
    if any(x in line for x in ['SEQ_INST.StopInProtein', 'SEQ_FEAT.FeatureBeginsOrEndsInGap','SEQ_FEAT.MisMatchAA','SEQ_FEAT.TransLen','SEQ_FEAT.AbuttingIntervals','SEQ_FEAT.TerminalXDiscrepancy','SEQ_FEAT.ShortIntron']):
        bad_contigs.append(line.split(accession_prefix)[1].split(':')[0]) # since it's always in the form PREFIX_VERSION_contig_numb
        bad_start.append(re.findall(r'\d+', line.split(accession_prefix)[1].split(':')[1].split('-')[0])[0]) # since it's always in the form ID:start-end
        bad_end.append(re.findall(r'\d+', line.split(accession_prefix)[1].split(':')[1].split('-')[1].split(']')[0])[0])
    if any(x in line for x in ['SEQ_INST.BadProteinStart','SEQ_INST.ShortSeq']):
        bad_names.append(line.split('gnl|Y1Q|')[1].split(':')[0])

# sometimes, the starting position > ending position, so correct these as needed:

bad_start_fixed = []
bad_end_fixed = []
for i in range(0,len(bad_start)):
    if (int(bad_start[i]) > int(bad_end[i])):
        bad_start_fixed.append(bad_end[i])
        bad_end_fixed.append(bad_start[i])
    else:
        bad_start_fixed.append(bad_start[i])
        bad_end_fixed.append(bad_end[i])

# match the Sequin names with locus tags in the gff file
bad_loci = []
k=0
for i in range(0, len(gffs)):
            contig_name = gffs[i].split(accession_prefix)[1].split(' ')[0]
            gene_start = gffs[i].split(' ')[3] # fourth column in GFF is always starting position 
            gene_end = gffs[i].split(' ')[4] # fifth column in GFF is always ending position
            if (any(x in gffs[i] for x in bad_names) or contig_name in bad_contigs and gene_start in bad_start_fixed and gene_end in bad_end_fixed):
                bad_loci.append(gffs[i].split('locus_tag=')[1].split(';')[0]) # there seems to be some duplicates occasionally showing up for some reason

keeper_lines = []
k = 0
for feature in gffs:
	k = k+1
	print(k)
	if (feature.split('locus_tag=')[1].split(';')[0]) not in bad_loci:
		keeper_lines.append(feature)

with open('cleaner.gff','w') as f:
	f.writelines(keeper_lines)


