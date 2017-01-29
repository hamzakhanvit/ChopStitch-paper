'''
Author : Hamza Khan
Usage : python evaluatedenovo_sg.py splicegraph
'''
from pprint import pprint
from Bio import SeqIO
import sys
import argparse, getopt


lst=[]
syn=[]
seqlen_dict={}
seq_dict={}
tp=0
fp=0
total = 0


def fasta_to_seqlen(filename, seqlen_dict):

  fasta_sequences = SeqIO.parse(open(filename),'fasta')
  for fasta in fasta_sequences:
        name, sequen = fasta.id, (fasta.seq.tostring())
        seq_dict[name]=sequen
        seqlen_dict[name]=len(sequen)




def readfile(filename, lst, syn):

   with open(filename, "r") as reader:
     line = (reader.readline()).strip().replace(';','')
     while(line):
       if(line.find('{')==-1 and line.find('}')==-1 ):
          splitted = (line.split('->'))
          lst.extend(splitted)
       line = (reader.readline()).strip().replace(';','')
   lst=list(set(lst))
   for items in lst:
     if "_OR_" in str(items):
        syn.append(((str(items).split("_OR_"))))         


def evaluate(syn, tp, fp, total):

   for item in syn:
       if(len(item) > 1):
           total+=1
           #print "\n\nItem = ", item
           length = 0
           biggest_exon=''
           failure_flag = 0
           for elements in item:
              if(int(seqlen_dict[elements]) > length):
                 length = int(seqlen_dict[elements])
                 biggest_exon = elements
           for elements in item:
              if((seq_dict[biggest_exon].find(seq_dict[elements])==-1)):
                 failure_flag = 1
                 break

           if(failure_flag == 1):
              fp+=1
              #print "failed case = ", item                 

           else:
              tp+=1           
        
 
   print "\nTrue Positives = ", tp
   print "\nFalse Positives = ", fp  
   print "\nTotal Nodes = ", total                   


def main(argv):
   if(len(argv)==0):
        print '\nERROR!:No input provided\n\nUsage: python evaluatedenovo_sg.py -i <FindExons splicegraph outputfile> -f <confident_exons.fa>'
        print "\nExample: python evaluatedenovo_sg.py -i <FindExons splicegraph outputfile> -f <confident_exons.fa>"
        sys.exit(2)
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:f:",["ifile=", "ffile="])
   except getopt.GetoptError:
      print __doc__,"\n",epi,'Usage: python evaluatedenovo_sg.py -i <FindExons splicegraph outputfile> -f <confident_exons.fa>'
      print "\nExample: python evaluatedenovo_sg.py -i <FindExons splicegraph outputfile> -f <confident_exons.fa>"
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print __doc__,"\n",epi,'Usage: python evaluatedenovo_sg.py -i <FindExons splicegraph outputfile> -f <confident_exons.fa>'
         print "\nExample: python evaluatedenovo_sg.py -i <FindExons splicegraph outputfile> -f <confident_exons.fa>"
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-f", "--ffile"):
         fastafile = arg
   print 'Input file is "', inputfile

   readfile(inputfile, lst, syn)
   #print syn

   fasta_to_seqlen(fastafile, seqlen_dict)
   #pprint(fasta_dict)
   evaluate(syn, tp, fp, total)
   #pprint(seqlen_dict)
   #pprint(seq_dict)
   #print syn



if __name__ == "__main__":

     main(sys.argv[1:])
