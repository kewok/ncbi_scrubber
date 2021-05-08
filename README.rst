NCBI Scrubber
==================

This is a collection of assorted python scripts that were created for cleaning the draft assembly and annotation based on errors flagged by NCBI. Many tasks, such as removing sequences < 200 bp, can be readily handled by existing tools (e.g., `seqkit <https://bioinf.shenwei.me/seqkit/>`_), and are not included here.

Basic workflow
----------------------------------

#. Assembly - rename sequences and purge contaminants/rejected sequences from your fasta file.
	* To rename a large number of sequence names to an NCBI compliant format, use ``id_rename.py`` to generate a new list of ids (``ids_new.txt``) and then search and replace the sequence names via

	``$seqkit replace --pattern "(.+)" -r "{kv}" -k ids_new.txt my_old.fasta > otcm.fasta``

	* To remove segments NCBI rejects:
		* copy and paste the sequence information flagged by NCBI into a csv file and run  ``$make_bed_file.py my_csv_generated.csv``. This will produce a file called ``bad.bed`` that specifies the regions to be masked 
		*  mask those regions with X using `bedtools <https://bedtools.readthedocs.io>`_

		``$bedtools maskfasta -fi input_sequence.fasta -bed bad.bed -fo sequence.fasta.out -mc X``

		* Replaces the 'X's with blanks using:

		``sed 's/X//g' sequence.fasta.out > sequence_excised.fasta``

	* If entire sequences/contigs need to be removed, identify them using ``make_contaminant_file.py``. This will produce a file called contaminant_sequences.txt and then these can be excised from the fasta file via:

	``seqkit grep --pattern-file contaminant_sequences.txt --invert-match input_sequence.fasta -o cleaned.fasta``

	* Identify the original sequence names in seqkit for the original (uncleaned) fasta file and for the fasta file that had the offending sequences removed, e.g.: 

	``seqkit seq --name input_sequence.fasta > ids_old.txt``
	``seqkit seq --name revised_cleaned.fasta > ids_cleaned.txt``

	* Match the new sequence ids to the old sequence ids using ``rematch_ids.py``. This generates a file called revised_name_table.txt. Rename the sequences in the fasta file:

	``seqkit replace --pattern "(.+)" -r "{kv}" -k revised_name_table.txt revised_cleaned.fasta > otcm.fasta``

	* Renumber sequences as needed using ``renumber.py``

#. Annotation - use these steps to fix issues in your discrepency report (.dr) and validation file (.val) after running `table2asn_gff <https://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/table2asn_GFF/>`_
	* Specify the first and last lines of your discrepency report containing the FATAL errors and extract these into a separate file using ``extract_lines.sh``

	* Identify the locus tags for problematic features by running ``extract_bad_features.py`` on the output of extract_lines.sh; this will create a file called ``bad_loci.txt.``

	* Purge those features via ``clean_gff_dr.py``

	* Find specific feature errors in your validation file and remove them using ``find_fix_seqfeat_errors.py``. Note you might have to add specific feature errors to the python script; as of May 10 2021 only ``SEQ_INST.StopInProtein`` is included
