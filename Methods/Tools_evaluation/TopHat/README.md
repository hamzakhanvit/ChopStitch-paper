Please install Bowtie2, TopHat, samtools and add their path to your .bashrc. 
         
Run_TopHat.sh has the commands to create Bowtie indexes from the reference genome file, align RNA-Seq reads against the genome using TopHat and sort and index BAM output files using Samtools.
    
```
Usage: 
    
sh Run_TopHat.sh [-r Reference Genome] [-i <Bowtie index filename for Reference genome>] [-g <Reference GTF file>] [-a <RNA-Seq PE FASTQ1>] [-b <RNA-Seq PE FASTQ2>] [-o <output directory>]
```
    
The final sorted BAM file is called accepted_hits.sorted.bam and will be present in the output folder.
