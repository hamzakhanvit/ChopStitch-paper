We aligned all putative exons outputted for *C. elegans* against their reference genome and hypothesized that all putative exons that are a part of a single node in a splice graph should align to approximately the same coordinates.
```         
------|-----------|-|--------------|---|------------|-|---------|------------------------------ GENOME

      -----Ex1----  -------Ex2-----    -----Ex3-----  ---Ex4---- Transcript 1

      -----Ex1----  -------Ex2-----                   ---Ex4---- Transcript 2    

      -----Ex1----  -------Ex2-----    -----Ex3-----  ---Ex4---- Reference Transcript a

      -----Ex1----  -------Ex2-----                   ---Ex4---- Reference Transcript b
```
                  
1) Exons constituting a splice node should map to the same location on the genome

2) (Extra check) All exons belonging to a single transcript in a splicegraph should have the same reference transcript mapping at the same location in the genome.

All nodes obeying these rules will be marked as true positive, while the others will be marked as false positives. 

       
####Run CreateBloom with the *C.elegans* real WGSS dataset mentioned in the manuscript.
     
####Download reference GFF3 file from [Ensembl](ftp://ftp.ensembl.org/pub/release-87/gff3/caenorhabditis_elegans) (Caenorhabditis_elegans.WBcel235.85.gff3).
```
grep "transcript" Caenorhabditis_elegans.WBcel235.85.gff3 > Caenorhabditis_elegans.WBcel235.85.gff3.bed
```
Our copy of Caenorhabditis_elegans.WBcel235.85.gff3.bed could be retrieved from this [link](https://drive.google.com/drive/folders/0B7WB43qKTdTZNmszYnZqZHZTOUE)      
    
####Using the generated Bloom filter, run FindExons with the TransABySS transcriptome assembly.(Click [here](https://drive.google.com/drive/folders/0B22DJq3IWQ8JeGpxZ2l3c1FWS0E) for our assembly file)
   
####Run MakeSplicegraph.py to generate a splicegraph file.
     
####Download a FASTA file of *C.elegans* reference genome. Click [here](https://drive.google.com/drive/folders/0B7WB43qKTdTZd2xydHBNRGl1ejg) to obtain our copy.
    
####Create bwa indices for the reference file
```
bwa index celegans_genome.fasta
```
    
####Align confident_exons.fa against the reference genome and generate a SAM alignment file
```
bwa mem -a celegans_genome.fasta confident_exons.fa > confident_exons.sam
```
    
####Run sam2coord.pl to convert SAM file to a coordinate file
````
perl /home/hkhan/Downloads/sam2coord.pl confident_exons.sam > confident_exons.coord
````
       
####Generate a bed file with mapping coordinates for each putative exon 
```
awk {'print $1,"\t",$6,"\t",$7,"\t",$8'} confident_exons.coord > sam2coord_assembled.bed
```
      
####Run compare_bed_celegans.py 
        
```
python compare_bed_celegans.py -i confident_exons_splicegraph -r Caenorhabditis_elegans.WBcel235.85.gff3.bed -b sam2coord_assembled.bed 

```
        
Output:
Total number of nodes      
True postive nodes         
False positive nodes          
