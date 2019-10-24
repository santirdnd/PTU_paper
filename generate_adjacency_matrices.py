#!/usr/bin/env python3

import os
import sys
import csv

os.makedirs('adjacency', exist_ok=True)

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

ani_all={}
fhr=open('ani_RefSeq84/RefSeq84_ani_p50_orig.tsv')
reader_ani=csv.DictReader(fhr, delimiter='\t')
for row in reader_ani:
    if row["Query genome"] not in ani_all:
        ani_all[row["Query genome"]]={}
    ani_all[row["Query genome"]][row["Reference genome"]]=row["ANI_tw"]
fhr.close()

for p1 in plasmid_all:
    for p2 in plasmid_all:
        if p2 not in ani_all[p1]:
            if p1 in ani_all[p2]:
                ani_all[p1][p2]=ani_all[p2][p1]
            else:
                ani_all[p1][p2]="0"
for p1 in plasmid_all:
    if len(ani_all[p1])!=len(plasmid_all):
        print("Error " + p1)

minhits_all={}
fhr=open('ani_RefSeq84/RefSeq84_ani_p50_orig.tsv')
reader_ani=csv.DictReader(fhr, delimiter='\t')
for row in reader_ani:
    if row["Query genome"] not in minhits_all:
        minhits_all[row["Query genome"]]={}
    minhits_all[row["Query genome"]][row["Reference genome"]]=row["min_hits"]
fhr.close()

for p1 in plasmid_all:
    for p2 in plasmid_all:
        if p2 not in minhits_all[p1]:
            if p1 in minhits_all[p2]:
                minhits_all[p1][p2]=minhits_all[p2][p1]
            else:
                minhits_all[p1][p2]="0"
for p1 in plasmid_all:
    if len(minhits_all[p1])!=len(plasmid_all):
        print("Error " + p1)

aniwf_max={}
fhr=open('ani_RefSeq84/RefSeq84_ani_p50_orig.tsv')
reader_ani=csv.DictReader(fhr, delimiter='\t')
for row in reader_ani:
    if row["Query genome"] == row["Reference genome"]:
        if int(row["Query size"]) <= 1000:
            aniwf_max[row["Query genome"]]=str(1)
        else:
            aniwf_max[row["Query genome"]]=str(1+((int(row["Query size"])-1000)//200))
fhr.close()

if len(aniwf_max)!=len(plasmid_all):
    print("Error ANIWF_MAX")

aniwf_all={}
fhr=open('ani_RefSeq84/RefSeq84_ani_p50_orig.tsv')
reader_ani=csv.DictReader(fhr, delimiter='\t')
for row in reader_ani:
    if row["Query genome"] not in aniwf_all:
        aniwf_all[row["Query genome"]]={}
    aniwf_all[row["Query genome"]][row["Reference genome"]]=str(int(row["ANI_tw_frag"])/min(int(aniwf_max[row["Query genome"]]),int(aniwf_max[row["Reference genome"]])))
fhr.close()

for p1 in plasmid_all:
    for p2 in plasmid_all:
        if p2 not in aniwf_all[p1]:
            if p1 in aniwf_all[p2]:
                aniwf_all[p1][p2]=aniwf_all[p2][p1]
            else:
                aniwf_all[p1][p2]="0"
for p1 in plasmid_all:
    if len(aniwf_all[p1])!=len(plasmid_all):
        print("Error " + p1)

af_ent={}
fhr=open('pANI_Enterobacterales/pANI.tsv')
reader_af=csv.DictReader(fhr, delimiter='\t')
for row in reader_af:
    if row["Query"] not in af_ent:
        af_ent[row["Query"]]={}
    af_ent[row["Query"]][row["Reference"]]=row["RW"]
fhr.close()

for p1 in plasmid_Ent:
    for p2 in plasmid_Ent:
        if p2 not in af_ent[p1]:
            if p1 in af_ent[p2]:
                af_ent[p1][p2]=af_ent[p2][p1]
            else:
                af_ent[p1][p2]="0"
for p1 in plasmid_Ent:
    if len(af_ent[p1])!=len(plasmid_Ent):
        print("Error " + p1)

fhw=open('adjacency/matrix_ANIp50_all.tsv','w')
for p1 in plasmid_all:
    if p1 != plasmid_all[0]:
        fhw.write("\n")
    for p2 in plasmid_all:
        if p2 != plasmid_all[0]:
            fhw.write("\t")
        fhw.write(ani_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_ANIp50_kept.tsv','w')
for p1 in plasmid_kept:
    if p1 != plasmid_kept[0]:
        fhw.write("\n")
    for p2 in plasmid_kept:
        if p2 != plasmid_kept[0]:
            fhw.write("\t")
        fhw.write(ani_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_ANIp50_Ent.tsv','w')
for p1 in plasmid_Ent:
    if p1 != plasmid_Ent[0]:
        fhw.write("\n")
    for p2 in plasmid_Ent:
        if p2 != plasmid_Ent[0]:
            fhw.write("\t")
        fhw.write(ani_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_ANIp50_EntGrd2.tsv','w')
for p1 in plasmid_EntGrd2:
    if p1 != plasmid_EntGrd2[0]:
        fhw.write("\n")
    for p2 in plasmid_EntGrd2:
        if p2 != plasmid_EntGrd2[0]:
            fhw.write("\t")
        fhw.write(ani_all[p1][p2])
fhw.close()

fhw=open('adjacency/matrix_minHitsp50_all.tsv','w')
for p1 in plasmid_all:
    if p1 != plasmid_all[0]:
        fhw.write("\n")
    for p2 in plasmid_all:
        if p2 != plasmid_all[0]:
            fhw.write("\t")
        fhw.write(minhits_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_minHitsp50_kept.tsv','w')
for p1 in plasmid_kept:
    if p1 != plasmid_kept[0]:
        fhw.write("\n")
    for p2 in plasmid_kept:
        if p2 != plasmid_kept[0]:
            fhw.write("\t")
        fhw.write(minhits_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_minHitsp50_Ent.tsv','w')
for p1 in plasmid_Ent:
    if p1 != plasmid_Ent[0]:
        fhw.write("\n")
    for p2 in plasmid_Ent:
        if p2 != plasmid_Ent[0]:
            fhw.write("\t")
        fhw.write(minhits_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_minHitsp50_EntGrd2.tsv','w')
for p1 in plasmid_EntGrd2:
    if p1 != plasmid_EntGrd2[0]:
        fhw.write("\n")
    for p2 in plasmid_EntGrd2:
        if p2 != plasmid_EntGrd2[0]:
            fhw.write("\t")
        fhw.write(minhits_all[p1][p2])
fhw.close()

fhw=open('adjacency/matrix_ANIWF_all.tsv','w')
for p1 in plasmid_all:
    if p1 != plasmid_all[0]:
        fhw.write("\n")
    for p2 in plasmid_all:
        if p2 != plasmid_all[0]:
            fhw.write("\t")
        fhw.write(aniwf_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_ANIWF_kept.tsv','w')
for p1 in plasmid_kept:
    if p1 != plasmid_kept[0]:
        fhw.write("\n")
    for p2 in plasmid_kept:
        if p2 != plasmid_kept[0]:
            fhw.write("\t")
        fhw.write(aniwf_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_ANIWF_Ent.tsv','w')
for p1 in plasmid_Ent:
    if p1 != plasmid_Ent[0]:
        fhw.write("\n")
    for p2 in plasmid_Ent:
        if p2 != plasmid_Ent[0]:
            fhw.write("\t")
        fhw.write(aniwf_all[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_ANIWF_EntGrd2.tsv','w')
for p1 in plasmid_EntGrd2:
    if p1 != plasmid_EntGrd2[0]:
        fhw.write("\n")
    for p2 in plasmid_EntGrd2:
        if p2 != plasmid_EntGrd2[0]:
            fhw.write("\t")
        fhw.write(aniwf_all[p1][p2])
fhw.close()

fhw=open('adjacency/matrix_AF_Ent.tsv','w')
for p1 in plasmid_Ent:
    if p1 != plasmid_Ent[0]:
        fhw.write("\n")
    for p2 in plasmid_Ent:
        if p2 != plasmid_Ent[0]:
            fhw.write("\t")
        fhw.write(af_ent[p1][p2])
fhw.close()
fhw=open('adjacency/matrix_AF_EntGrd2.tsv','w')
for p1 in plasmid_EntGrd2:
    if p1 != plasmid_EntGrd2[0]:
        fhw.write("\n")
    for p2 in plasmid_EntGrd2:
        if p2 != plasmid_EntGrd2[0]:
            fhw.write("\t")
        fhw.write(af_ent[p1][p2])
fhw.close()
