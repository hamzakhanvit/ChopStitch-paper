Please install StringTie and add its path to your .bashrc
   
```
Usage:sh Run_StringTie.sh [-a <Run_TopHat.sh output file accepted_hits.bam>]
```
One of the output files called stringtie-results has putative exons coordinates in it. 
    
Run this AWK command to extract a BED file of putative exons
```
awk {'if($3=="exon") print $1"\t"$4-1"\t"$5'} stringtie-results > stringtie-exons.bed
```
          
Use bedtools to extract a FASTA file of putative exons from stringtie-exons.bed and a reference genome FASTA file:
````
bedtools getfasta -fi <input reference FASTA> -bed <stringtie-exons.bed> -fo <stringtie-exons.fa>
````
     
