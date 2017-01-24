#!/usr/bin/env python
"""
Check Splice Graph made by ChopStitch with ensembl reference transcripts 
"""
from __future__ import division
import argparse, datetime, csv
import sys, getopt
from pprint import pprint


ts = datetime.datetime.now()

__title__ = 'Splicegraph ensembl Validation'
__version__ = '0'
__description__ = "Check Splice Graph made by ChopStitch with ensembl reference transcripts"
__author__ = 'Hamza Khan'
__license__ = 'GPL license'
__author_email__ = "hamzakhanvit@gmail.com"
epi = "Licence: %s by %s <%s>\n\n" % (__license__,
__author__,
__author_email__)
__doc__ = "***************************************************************\
          \n %s v%s - %s \n************************************************\
***************" % (__title__,
__version__,
__description__)

subGr = {}
transcripts = {}
nodes = {}
ref = {}
Subgraph_eval = {}

def readfile(inputfile):
     

    handle = open(inputfile, 'r')
    for line in handle:
         cc = line.split("subgraphgraphname_cc_")
    
    #Remove the first item which is empty     
    cc=cc[1:]   
  
    #Remove the last bracket
    cc[len(cc)-1] = cc[len(cc)-1][:-1]  
 
    for i in cc:
        temp = i.split("{")
        subGr[temp[0]] = (temp[1].split(';'))[:-1]
        transcripts[temp[0]] = []
        nodes[temp[0]] = []
        for items in subGr[temp[0]]:
            node = items.split("->")
            nodes[temp[0]].extend(node)
            for x in node:
                if("_OR_") in x:
                   trans = x.split("_OR_")
                   #print(trans)
                   for y in trans:
                       a = y.split("_")
                       transcripts[temp[0]].append(a[0])   
                else:
                   a = x.split("_")
                   transcripts[temp[0]].append(a[0]) 
        subGr[temp[0]] = list(set(subGr[temp[0]]))                           
        nodes[temp[0]] = list(set(nodes[temp[0]]))
        transcripts[temp[0]] = list(set(transcripts[temp[0]])) 

    #pprint(subGr)
    #pprint(nodes)
    ##pprint(transcripts)

    
def readReference(referencefile):
    ''' 
    Read reference file of transcript-gene pairs
    '''
    h = open(referencefile, 'r')
    for line in h:
       line.rstrip()
       temp = line.split("\t")
       ref[(temp[0].split('.')[0][1:])] = (temp[1].split('.'))[0]
    #pprint(ref)


def checkTranscripts():
    
    for i in xrange(0,101):
         Subgraph_eval[i]=0

    error_subgraph=0
    for subgraph in transcripts:
       TP = 0
       FP = 0
       l = []
       ##print "SUBGRAPH ",subgraph,"\n\n" 
       error_trans = 0
       for transcript in transcripts[subgraph]:
           #print "transcript=",transcript

           if transcript not in ref:
                #print "This transcript not in reference=",transcript
                error_trans+=1
                continue
           else:
                #print "reference gene =", ref[transcript]
                l.append(ref[transcript])

       if (error_trans>0):
           error_subgraph+=1
           continue
       gene_count = []
       for gene in l:
           gene_count.append(l.count(gene))
       #print "gene count = ", gene_count
       m = max(gene_count)
       p = int((m/len(l))*100) 
       ##print "Max count", m
       ##print "Percentage = %.2f " % p   

       #Checking splicegraphs that had 50% percentage
       #if(p==50):
            #print ("\n\nSplice graph no. %s has 50 percent transcripts "% subgraph)
            #print (set(l))


       Subgraph_eval[p] = Subgraph_eval[p] + 1
    print Subgraph_eval 
    print "Subgraphs with error = ", error_subgraph
    
    with open('Subgraph_eval.out', 'w') as f:
         f.write("Percentage, Number of splice subgraphs\n")
         for keys in Subgraph_eval:
             s = str(keys) + "," + str(Subgraph_eval[keys])+"\n"
             f.write(s)


def main(argv):
   if(len(argv)==0):
        print '\nERROR!:No input provided\n\nUsage: python splicegraph_ensembl_validation.py -i <formatted_splicesubgraphs> -r <transcript-gene-file>'
        print "\nExample: python splicegraph_ensembl_validation.py -i splicegraph_formatted -r transcript_gene_pairs"
        sys.exit(2)
   inputfile = ''
   referencefile = 'transcript_gene_pairs'
   try:
      opts, args = getopt.getopt(argv,"hi:r:",["ifile=","rfile="])
   except getopt.GetoptError:
      print __doc__,"\n",epi,'Usage: python splicegraph_ensembl_validation.py -i <formatted_splicesubgraphs> -r <transcript-gene-file>'
      print "\nExample: python splicegraph_ensembl_validation.py -i splicegraph_formatted -r transcript_gene_pairs"
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print __doc__,"\n",epi,'Usage: python splicegraph_ensembl_validation.py -i <inputfile> -r <referencefile>'
         print "\nExample: python splicegraph_ensembl_validation.py -i splicegraph_formatted -r transcript_gene_pairs"
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-r", "--rfile"):
         referencefile = arg
   print 'Input file is "', inputfile
   print 'reference file is "', referencefile
 
   readfile(inputfile)
   readReference(referencefile)
   checkTranscripts()
   #checkNodes()

   tf = datetime.datetime.now()
   print "\n Time required - ",tf-ts


if __name__ == "__main__":
   main(sys.argv[1:])


