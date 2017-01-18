Please make sure that [TransABySS](http://www.bcgsc.ca/platform/bioinfo/software/trans-abyss) is correctly installed and the required paths have been added to .bashrc

```     
Usage: sh TransABySS.sh [-p <Path to output directory>] [-t <Number of threads>] [-f <FASTQ1 FASTQ2>]
        
-p : Path to the output directory
-t : Number of threads
-f : Paired end FASTQ files separated by single space
```
       
This script runs TransABySS for k values 25, 35 and 45, merges the individual assemblies using TransABySS merge and removes contigs of length less than 100 nucleotides. 
     
The final output assembly FASTA file is k25_35_45_100+.fa and can be downloaded from this [link.](https://drive.google.com/drive/folders/0B22DJq3IWQ8JeGpxZ2l3c1FWS0E)
