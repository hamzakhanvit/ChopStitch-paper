#!/usr/bin/env python
"""
extract_exons_from_LEMONS_output
"""

import argparse, datetime
import sys, getopt

ts = datetime.datetime.now()

__title__ = 'Extract LEMONS exons'
__version__ = '0'
__description__ = "extract_exons_from_LEMONS_output"
__author__ = 'Hamza Khan'
__license__ = 'GPL license'
__author_email__ = "hkhan@bcgsc.ca"
epi = "Licence: %s by %s <%s>\n\n" % (__license__,
__author__,
__author_email__)
__doc__ = "***************************************************************\
          \n %s v%s - %s \n************************************************\
***************" % (__title__,
__version__,
__description__)



def extract_exons(inputfile, outputfile):
   '''
   Given an input xls file from LEMONS, 
   it outputs a FASTA file of putative exons
   '''
   f=open(inputfile,'r')
   w=open(outputfile,'w')
   for line in f:
       line=line.rstrip()
       lst=line.split("\t")
       exons=lst[3].split('@')
       for i in xrange(len(exons)):
         if(exons[i]!=''):
             if(exons[i][0].isupper()):
                s=">"+str((lst[0].split("_"))[0])+"_exonNo."+str(i)+"-length_"+str(len(exons[i]))+"\n"+exons[i]+"\n"
                w.write(s)
               
      
def main(argv):
   if(len(argv)==0):
        print '\nERROR!:No input provided\n\nUsage: python extractLEMONSexons.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
   inputfile = ''
   outputfile = 'LEMONS_EXONS.fa'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print __doc__,"\n",epi,'Usage: python extractLEMONSexons.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print __doc__,"\n",epi,'Usage: python extractLEMONSexons.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   extract_exons(inputfile, outputfile)    


if __name__ == "__main__":
   main(sys.argv[1:])


