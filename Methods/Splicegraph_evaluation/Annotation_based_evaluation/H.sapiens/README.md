Subgraphs obtained after running Graphviz ccomps represent different
transcript isoforms for a single gene. We expect all exons in a splicesubgraph
to come from the same gene. Using Ensembl reference transcripts
along with experimental WGSS data as inputs to ChopStitch, we did the following analysis - 
       
####Run CreateBloom with the *H.sapiens* real WGSS dataset mentioned in the manuscript.
     
####Download reference transcripts FASTA file from [Ensembl](ftp://ftp.ensembl.org/pub/release-87/fasta/homo_sapiens/cdna/) (Homo_sapiens.GRCh38.cdna.all.fa). Our downloaded copy could be retrieved from this [link](https://drive.google.com/drive/folders/0B7WB43qKTdTZbHlBd1FwM2ZfclU)      
    
####Using the generated Bloom filter, run FindExons with Homo_sapiens.GRCh38.cdna.all.fa.
   
####Run MakeSplicegraph.py and ccomps to generate a splice subgraph file.    
       
####Run formatc.sh to format your splice subgraph file and to extract gene and transcript IDs from the headers of Homo_sapiens.GRCh38.cdna.all.fa            
   
```
sh formath.sh -s splice_subgraph -r Homo_sapiens.GRCh38.cdna.all.fa      
```
Output:   
splicegraph_formatted - A formatted splice subgraph file   
transcript_gene_pairs - A file containing gene and transcript IDs pairs extracted from the headers of Homo_sapiens.GRCh38.cdna.all.fa             

####Run splicegraph_ensembl_validation.py    
```
python splicegraph_ensembl_validation.py -i splicegraph_formatted -r transcript_gene_pairs      
```
Output:    
[Subgraph_eval.out](./Subgraph_eval.out) - A CSV file with two columns :     
* The percentage of transcripts in a splice subgraph that belong to a single gene       
* Number of splice subgraphs for a particular precentage.      
