We expect all putative exons that form a single node in a splice graph to be substrings of the longest putative exon in that node.

```
python evaluatedenovo_sg.py -i <MakeSplicegraph.py_output_splicegraph> -f <FindExons_FASTA_output>
```
For example-   
```
python evaluatedenovo_sg.py -i confident_exons_splicegraph -f confident_exons.fa
```
     
Output:
Total nodes         
True positive nodes     
False positive nodes    



