import csv
import re, sys
import argparse, getopt
from collections import defaultdict

def readfile(filename, lst, syn):
   #print filename
   with open(filename, "r") as reader:
     line = (reader.readline()).strip().replace(';','')
     while(line):
          if(line.find('{')==-1 and line.find('}')==-1 ):
             #print(line)
             splitted = (line.split('->'))
             #print splitted
             lst.extend(splitted)
          #print lst
          line = (reader.readline()).strip().replace(';','')
   lst=list(set(lst))
   #print "lst = " , lst

   for items in lst:
       if "_OR_" in str(items):
           syn.append((str(items).split("_OR_")))         
   #syn=[list(x) for x in set(tuple(x) for x in syn)]
   #print "syn = ", syn
   return syn 



def main(argv):
   if(len(argv)==0):
        print '\nERROR!:No input provided\n\nUsage: python compare_bed_celegans.py -i <splicegraph> -b <sam2coord_assembled.bed>'
        print "\nExample: python compare_bed_celegans.py -i <splicegraph> -b <sam2coord_assembled.bed>"
        sys.exit(2)
   inputfile = ''
   alignmentfile = 'sam2coord_assembled.bed'
   try:
      opts, args = getopt.getopt(argv,"hi:r:b:",["ifile=","rfile=","bfile="])
   except getopt.GetoptError:
      print __doc__,"\n",epi,"Usage : python compare_bed_celegans.py -i <splicegraph> -b <sam2coord_assembled.bed>"
      print "\nExample : python compare_bed_celegans.py -i <splicegraph> -b <sam2coord_assembled.bed>"
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print __doc__,"\n",epi,'Usage : python compare_bed_celegans.py -i <splicegraph> -b <sam2coord_assembled.bed>'
         print "\nExample : python compare_bed_celegans.py -i <splicegraph> -b <sam2coord_assembled.bed>"
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-b", "--bfile"):
         alignmentfile = arg

   print 'Input file is ', inputfile
   print 'Alignment file is ',  alignmentfile



   hand = open(alignmentfile, "rU")
   d = defaultdict(list)
   dref = defaultdict(list)
   #csvfile = open('compare_bed.out', 'wb')
   #w = csv.writer(csvfile, delimiter=',')


   for line in hand:
     myarr=[]
     words=[]
     if ('\t' in line):
       word = line.split('\t')
       for x in word:
          words.append(x.strip())
       #print words
       if ((len(words) == 4 and words[2] and words[3] and  (words[1]).split('|')[3][:-3] in (['NC_000001', 'NC_000002', 'NC_000003', 'NC_000004', 'NC_000005', 'NC_000006', 'NC_000007', 'NC_000008', 'NC_000009', 'NC_000010', 'NC_000011', 'NC_000012', 'NC_000013', 'NC_000014','NC_000015', 'NC_000016', 'NC_000017', 'NC_000018', 'NC_000019', 'NC_000020', 'NC_000021', 'NC_000022', 'NC_000023', 'NC_000024']))):
          trans_id = (words[0]).strip()
          #print trans_id
          if ('|' in words[1]):  
              ref_id = (words[1]).split('|')
              #print ref_id[3]
              myarr.extend((ref_id[3][:-3],words[2],(words[3].rstrip('\n'))))
          #print myarr, "\n\n\n"
          d[trans_id].append(myarr) 


   #print "Lets see how our sam2coord dictionary looks like\n\n"
   #for key in d:
       #print "sam2coord", key, "\n"
       #print d[key], "\n\n"


   #Making the dicitonary unique
   d2 = defaultdict(list)
   for key in d:
       tmp=[]
       for lista in d[key]:
         if(lista not in tmp):
            d2[key].append(lista)
            tmp.append(lista)


   total_nodes =0
   tp_nodes = 0
   fp_nodes = 0
   fn_nodes = 0
   lst=[]
   syn=[]
   syn = readfile(inputfile, lst, syn)
   count=0
   for item in syn:
      if(len(item) > 1):
         count+=1
      flag=0
      check=1
      found=0
      first_exon=item[0]
      #print "\nFirst_Exon = ",first_exon,"\n"
      #print "\nd2[first_exon]", d2[first_exon]
      for maps in d2[first_exon]:
        if(found==0):
          #print maps
          if(maps[0] in ['NC_000001', 'NC_000002', 'NC_000003', 'NC_000004', 'NC_000005', 'NC_000006', 'NC_000007', 'NC_000008', 'NC_000009', 'NC_000010', 'NC_000011', 'NC_000012', 'NC_000013', 'NC_000014','NC_000015', 'NC_000016', 'NC_000017', 'NC_000018', 'NC_000019', 'NC_000020', 'NC_000021', 'NC_000022', 'NC_000023', 'NC_000024'] ):        
               chrom=maps[0]
               start=int(maps[1])
               end=int(maps[2])
          else:
            fp_nodes+=1
            break
          for exon in xrange(1,len(item)):
             #print "\nexon=", item[exon]
             if(item[exon] not in d2):
                 flag=1;
                 #print "\nNot d2 exon=", item[exon]
                 break;
             for mapps in d2[item[exon]]:
                   chrom2=mapps[0]
                   start2=int(mapps[1])
                   end2=int(mapps[2])
                   if(chrom2==chrom and start2 in range(start-6,start+5,1) and end2 in range(end-6, end+5,1)):
                      check+=1
                      #print "\nfirst_exon=", first_exon, "chrom=", chrom," start=",start," end=",end, "\n chrom2=", chrom2, " start2=",start2," end2=",end2, " check=", check,"\n"
                      break    
                   else:
                      pass
                      #print "\nNEGATIVE-first_exon=", first_exon, "chrom=", chrom," start=",start," end=",end, "\n chrom2=", chrom2, " start2=",start2," end2=",end2, "\n"                                    
          if(flag==0 and check>=len(item)):
             found=1         

 
      if(flag==1):
         fp_nodes+=1
      if(flag==0 and check>=len(item)):
         tp_nodes+=1
         #print "TRUEPOSITIVE "
      if(flag==0 and check<len(item)): 
         fp_nodes+=1   
         #print "FALSE"
      

   print "\n\nTotal=", count
   print "\n\nTP_nodes=", tp_nodes
   print "\n\nFP_nodes=", fp_nodes


if __name__ == "__main__":
   main(sys.argv[1:])
