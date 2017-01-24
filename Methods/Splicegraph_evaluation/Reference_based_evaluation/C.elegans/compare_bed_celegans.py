#hand = open("sam2coord_without_a.bed", "rU")
hand = open("sam2coord_assembled.bed", "rU")
ref = open("Caenorhabditis_elegans.WBcel235.85.gff3.bed", "rU")
from collections import defaultdict
d = defaultdict(list)
dref = defaultdict(list)

import csv
import re
csvfile = open('compare_bed.out', 'wb')
w = csv.writer(csvfile, delimiter=',')

def readfile(filename, lst, syn):
   print filename
   with open(filename, "r") as reader:
     line = (reader.readline()).strip().replace(';','')
     while(line):
          #if(line.find('{')==-1 and line.find('}')==-1 ):
          #print(line)
          splitted = (line.split('->'))
          #print splitted
          lst.extend(splitted)
          #print lst
          line = (reader.readline()).strip().replace(';','')
 
   #print "lst = " , lst

   for items in lst:
       if "_OR_" in str(items):
           syn.append((str(items).split("_OR_")))         
   syn=[list(x) for x in set(tuple(x) for x in syn)]
   print "syn = ", syn
   return syn 




for line in hand:
  myarr=[]
  if ('\t' in line):
    words = line.split('\t')
    if ((len(words) == 4 and (words[1]).strip() in  ['I','II','III','IV','V','X', 'MtDNA'] and words[2]!='' and words[3]!='')):
       trans_id = (words[0]).strip()
       #print trans_id
       ref_id = (words[1]).strip()
       #print ref_id        
       myarr.extend((ref_id,words[2].strip(),(words[3].rstrip('\n'))))
       #print myarr, "\n\n\n"
       d[trans_id].append(myarr)
#print d, "\n\n\n"  

'''
print "Lets see how our sam2coord dictionary looks like\n\n"
for key in d:
    print "sam2coord", key, "\n"
    print d[key], "\n\n"
'''

#Making the dicitonary unique
d2 = defaultdict(list)
for key in d:
    tmp=[]
    for lista in d[key]:
      if(lista not in tmp):
         d2[key].append(lista)
         tmp.append(lista)

for line in ref:
  st = ""
  refarr=[]
  if ('\t' in line):
    row_words = line.split('\t')
    if (len(row_words) == 4):
       m = re.search('(transcript:)(.*?)(\;){1}', row_words[0])
       if m:    
        st = m.group(0)
        st = st[11:]
        st = st[:-1]
        #print st
    refarr.extend((row_words[1],row_words[2],(row_words[3].rstrip('\n'))))
  dref[st].append(refarr)

'''
print "Lets see how our reference dictionary looks like\n\n"

for key in dref:
    print "Reference ",key, "\n"
    print dref[key], "\n\n\n"
'''


total_nodes =0
tp_nodes = 0
fp_nodes = 0
fn_nodes = 0
lst=[]
syn=[]
syn = readfile("../confident_exons_splicegraph", lst, syn)
count=0
for item in syn:
   count+=1
   flag=0
   check=1
   found=0
   first_exon=item[0]
   print "\nFirst_Exon = ",first_exon,"\n"
   print "\nd2[first_exon]", d2[first_exon]
   for maps in d2[first_exon]:
     if(found==0):
       print maps
       if(maps[0] in ['I','II','III','IV','V','X', 'MtDNA'] ):        
            chrom=maps[0]
            start=int(maps[1])
            end=int(maps[2])
       else:
         fp_nodes+=1
         break
       for exon in xrange(1,len(item)):
          print "\nexon=", item[exon]
          if(item[exon] not in d2):
              flag=1;
              print "\nNot d2 exon=", item[exon]
              break;
          for mapps in d2[item[exon]]:
                chrom2=mapps[0]
                start2=int(mapps[1])
                end2=int(mapps[2])
                if(chrom2==chrom and start2 in range(start-6,start+5,1) and end2 in range(end-6, end+5,1)):
                   check+=1
                   print "\nfirst_exon=", first_exon, "chrom=", chrom," start=",start," end=",end, "\n chrom2=", chrom2, " start2=",start2," end2=",end2, " check=", check,"\n"
                   break    
                else:
                   print "\nNEGATIVE-first_exon=", first_exon, "chrom=", chrom," start=",start," end=",end, "\n chrom2=", chrom2, " start2=",start2," end2=",end2, "\n"                                    
       if(flag==0 and check>=len(item)):
          found=1         

 
   if(flag==1):
      fp_nodes+=1
   if(flag==0 and check>=len(item)):
      tp_nodes+=1
      print "TRUEPOSITIVE "
   if(flag==0 and check<len(item)): 
      fp_nodes+=1   
      print "FALSE"
      

print "\n\nTotal=", count
print "\n\ntp_nodes=", tp_nodes
print "\n\nfp_nodes=", fp_nodes

'''
#for key in d:
 #   print "Key is ", key, "\n"
  #  print "In dict d values are ", d[key], "\n";
   # print "In dict dref values are ", dref[key], "\n";
done_key=[]
total =0
tp_exons = 0
fp_exons = 0
fn_exons = 0
for key in d2:
  if key in dref:
    print key
    if(key not in done_key):
      done_key.append(key)
      exons_in_d2 = len(d2[key]);
      exons_in_dref = len(dref[key])-1;
      print "\n\n\n\n\n\n",key,"\n\n"
      print exons_in_d2, "\n\n", exons_in_dref
      #print d[key],"\n\n",dref[key] 
      matches = 0 
      for lista in (d2[key]):
        if(len(lista)==3):
            for listb in (dref[key]):
               #print type(str(lista[0]))," ====== ", type(str(listb[0])),"\n"
               #print "lista[1] = ",lista[1] ,"\n",range((int(listb[1])-6),(int(listb[1])+5),1 ),"\n"; 
              #if((str(lista[0]) == str(listb[0])) and (int(lista[1]) in range((int(listb[1])-6),(int(listb[1])+5),1 )) and (int(lista[2]) in range((int(listb[2])-6),(int(listb[2])+5),1 ))):
               if((str(lista[0])) in (str(listb[0])) and (int(lista[1]) in range((int(listb[1])-6),(int(listb[1])+5),1 ))and (int(lista[2]) in range((int(listb[2])-6),(int(listb[2])+5),1 ))):
                 #print key, "\n", lista[0],listb[0], "\n",lista[1],listb[1], "\n",lista[2], listb[2],"\n\n\n"
                 tp_exons = tp_exons + 1;
                 matches = matches + 1;
      if(exons_in_d2 > matches):
         fp_exons = fp_exons + (exons_in_d2 - matches);
      if(exons_in_dref > tp_exons):
         fn_exons = fn_exons + (exons_in_dref - matches);          
      for count in dref[key]:
         total = total+1;     
      total = total-1;
print "\n\n Total exons in reference file = ", total;
print "\n\n Matched or TP exons in reference file = ", tp_exons;
print "\n\n FP_exons = ",fp_exons;
print "\n\n FN_exons = ", fn_exons;
 
'''
