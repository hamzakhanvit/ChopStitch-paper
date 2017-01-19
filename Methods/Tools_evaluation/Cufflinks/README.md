Please install Cufflinks and add its path to your .bashrc
   
```
Usage:sh Run_Cufflinks.sh [-a <Run_TopHat.sh output file accepted_hits.bam>]
```
One of the output files called transcripts.gtf has putative exons coordiates in it. 
    
Run this AWK command to extract a BED file of putative exons
```
awk {'if($3=="exon"){print $1"\t"$4-1"\t"$5}'} transcripts.gtf > cufflinks_exons.bed
```
          
Use bedtools to extract a FASTA file of putative exons from cufflinks_exons.bed and the reference genome FASTA file:
````
bedtools getfasta -fi <input reference FASTA> -bed <cufflinks_exons.bed> -fo <Putative-Exons.fa>
````
     
