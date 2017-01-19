Run-LEMONS.sh is a shell script to run LEMONS. Download LEMONS and add LEMONS.py to your .bashrc.
```
Usage: 
sh Run-LEMONS.sh -f <transcriptome assembly file>
```
One of the output is *k25_35_45_merged_100+.fa_2_D.rerio_1_H.sapiens_4_G.gallus_6_X.tropicalis_D.melanogaster_A.thaliana_5_A.carolinensis_3_M.musculus_C.elegans_Merged.xls* which contains information on the number of identified exons, their lengths and sequences. 
     
Run extractLEMONSexons.py to extract putative exons in a FASTA file with headers in the following format - 
TranscriptID_exonNo.x-length_y
```
Usage:
python extractLEMONSexons.py -i <input_xls_file> -o <output_FASTA_file>
```
