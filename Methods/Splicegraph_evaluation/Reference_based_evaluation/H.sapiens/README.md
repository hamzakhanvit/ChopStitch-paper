We aligned all putative exons outputted for *H.sapiens* against its reference genome and hypothesized that all putative exons that are a part of a single node in a splicegraph should align to approximately the same coordinates.
```         
------|-----------|-|--------------|---|------------|-|---------|------------------------------ GENOME

      -----Ex1----  -------Ex2-----    -----Ex3-----  ---Ex4---- Transcript 1

      -----Ex1----  -------Ex2-----                   ---Ex4---- Transcript 2    

```
                            

All nodes obeying this rule will be marked true positive, while the others will be marked as false positives. 
             
       
####Run CreateBloom with the *H.sapiens* real WGSS dataset mentioned in the manuscript.
         
####Using the generated Bloom filter, run FindExons with the TransABySS transcriptome assembly.(Click [here](https://drive.google.com/drive/u/1/folders/0B22DJq3IWQ8JX2xaTXZqVFZGNFE) for our assembly file)
   
####Run MakeSplicegraph.py to generate a splicegraph file.
     
####Download a FASTA file of *H.sapiens* reference genome from NCBI. Click [here](https://drive.google.com/drive/u/1/folders/0B7WB43qKTdTZZ3VSd1ZGSkVlWXc) to obtain our copy.
    
####Create bwa indices for the reference file
```
bwa index NCBI_assembled_hs_ref_GRCh38.fna
```
    
####Align confident_exons.fa against the reference genome and generate a SAM alignment file
```
bwa mem -a NCBI_assembled_hs_ref_GRCh38.fna confident_exons.fa > confident_exons.sam
```
    
####Run sam2coord.pl to convert SAM file to a coordinate file
````
perl sam2coord.pl confident_exons.sam > confident_exons.coord
````
       
####Generate a bed file with mapping coordinates for each putative exon
``` 
awk {'print $1,"\t",$6,"\t",$7,"\t",$8'} confident_exons.coord > sam2coord_assembled.bed
```
              
####Run compare_bed_human.py 
```
python compare_bed_human.py -i confident_exons_splicegraph -b sam2coord_assembled.bed
```
        
Output:
Total number of nodes  	   
True postive nodes     	   
False positive nodes   	      

