#!/usr/bin/env python3

import os
import sys
import csv

with open('plasmid.lst') as fh:
    plasmid_all=[]
    for line in fh:
        plasmid_all.append(line.strip())
with open('plasmid_kept.lst') as fh:
    plasmid_kept=[]
    for line in fh:
        plasmid_kept.append(line.strip())
with open('plasmid_bad.lst') as fh:
    plasmid_bad=[]
    for line in fh:
        plasmid_bad.append(line.strip())
with open('plasmid_Enterobacterales.lst') as fh:
    plasmid_Ent=[]
    for line in fh:
        plasmid_Ent.append(line.strip())
with open('plasmid_EnterobacteralesGrd2.lst') as fh:
    plasmid_EntGrd2=[]
    for line in fh:
        plasmid_EntGrd2.append(line.strip())

aniwf_max={}
with open('ani_RefSeq84/RefSeq84_ani_p50_orig.tsv') as fhr:
    reader_ani=csv.DictReader(fhr, delimiter='\t')
    for row in reader_ani:
        if row["Query genome"] == row["Reference genome"]:
            if int(row["Query size"]) <= 1000:
                aniwf_max[row["Query genome"]]=str(1)
            else:
                aniwf_max[row["Query genome"]]=str(1+((int(row["Query size"])-1000)//200))

if len(aniwf_max)!=len(plasmid_all):
    print("Error ANIWF_MAX")

fhr=open('ani_RefSeq84/RefSeq84_ani_p50_orig.tsv')
fhw=open('ani_RefSeq84/RefSeq84_ANI-WF_orig.tsv','w')
header='\t'.join(("Query genome", "Reference genome", "Query size", \
                  "Reference size", "Query AWFmax", "Reference AWFmax", \
                  "min_hits", "ANI_tw", "ANI_tw_SD", "ANI_tw_frag", "AWF"))
fhw.write(header+"\n")
reader_ani=csv.DictReader(fhr, delimiter='\t')
for row in reader_ani:
    line='\t'.join((row["Query genome"], row["Reference genome"], \
                    row["Query size"], row["Reference size"], \
                    aniwf_max[row["Query genome"]], \
                    aniwf_max[row["Reference genome"]], row["min_hits"], \
                    row["ANI_tw"], row["ANI_tw_SD"], row["ANI_tw_frag"], \
                    str(int(row["ANI_tw_frag"])/min(int(aniwf_max[row["Query genome"]]),int(aniwf_max[row["Reference genome"]])))))
    fhw.write(line+"\n")
fhr.close()
fhw.close()
