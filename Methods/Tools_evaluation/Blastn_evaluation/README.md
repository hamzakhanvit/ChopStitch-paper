###Download Reference Exons
We downloaded reference exons from [Ensembl BioMart](http://www.ensembl.org/biomart/martview/) for *C.elegans* and *H.sapiens*
     
The downloaded reference exons can be retrieved from this [link](https://drive.google.com/drive/folders/0B22DJq3IWQ8JRHVIcU9SQ1JoRTQ)
   
###Create Blast databases
We created blast databases from the reference exons using the command - 
```
makeblastdb -in <Reference exons FASTA file>  -dbtype nucl -out <Ref exons BlastDB name>
``` 
     
###Run Blastn with putative exons ouputted from each tool (ChopStitch, LEMONS, StringTie and Cufflinks) as 'Query' against 'Reference exons BlastDB'
```
blastn -num_threads 80 -db <Ref exons BlastDB name> -query <Putative exons FASTA file from a tool> -out blast.out -outfmt "6 qseqid sseqid qlen qstart qend qseq slen sstart send sseq evalue bitscore score pident qcovs"
```
    
###Find number of a Tool's putative exons with hits to reference exons at a sequence identity and coverage of 95% and a length difference of 5 or less than 5 between subject and query sequences:
```
awk '{if($14 >=95 && $15 >=95 && $3>=($7-5) && $3<=($7+5) && ($5-$4)>=($3-5) && ($5-$4)<=($3+5) ) print $1;}' blast.out | sort | uniq | wc -l
```
These hits were considered as True Positives. (See supplementary table 2, 3)
         
###Total number of a tool's putative exons:
```
grep ">" Putative_exons_FASTA_file | wc -l
```
    
###Total number of Ensembl reference exons:
```
grep ">" Ensembl_exons_FASTA_file | wc -l
```

###Find number of Reference exons with hits to a tool's putative exons at a sequence identity and coverage of 95% and a length difference of 5 or less than 5 between subject and query:
```
awk '{if($14 >=95 && $15 >=95 && $3>=($7-5) && $3<=($7+5) && ($5-$4)>=($3-5) && ($5-$4)<=($3+5) ) print $2;}' blast.out | sort | uniq | wc -l
```
The total number of reference exons minus the number of hits from the above query were considered as False negatives. (See Supplementary table 2,3)   
    
For Precision, sensitivity calculation please refer to Supplementary table 2,3.
