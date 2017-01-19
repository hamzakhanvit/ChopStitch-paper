Install ChopStitch, Graphviz cmd tools and add its path to your .bashrc. 
    
###Run CreateBloom
```
./CreateBloom -t 32 -k 50 --fpr1 0.16 --fpr2 0.01 <FASTQ1> <FASTQ2>
```
        
###Run FindExons
```
./FindExons -i <input Bloom Filter file(Bfilter.bf)> <Transcriptome assembly file in TransABySS FASTA format>
```

###Run MakeSplicegraph.py with the putative exons FASTA file outputted by FindExons(confident-exons.fa)
```
python MakeSplicegraph.py -i <inputfile> -o <Splicegraph-outputfile>
```
    
###Run Graphviz ccomps to obtain Splice sub-graphs
```
ccomps <Splicegraph DOT file from MakeSplicegraph.py> -o <splicegraph_subgraph>
```
