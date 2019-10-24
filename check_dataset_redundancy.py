#!/usr/bin/env python3

import os
import sys
import csv

ptus={}
plasmids={}

fhr=open('plasmid_mob_pfinder_pGroup_filt.tsv')
pl_reader=csv.DictReader(fhr, delimiter='\t')
for row in pl_reader:
    if row["pGroup"] not in ptus:
        ptus[row["pGroup"]]=[]
    ptus[row["pGroup"]].append(row["AccessionVersion"])
    plasmids[row["AccessionVersion"]]={"Size":row["Size"], "pGroup":row["pGroup"]}
fhr.close()

isolengths=[]
for ptu in ptus:
    lengths={}
    for pl in ptus[ptu]:
        if plasmids[pl]["Size"] not in lengths:
            lengths[plasmids[pl]["Size"]]=[]
        lengths[plasmids[pl]["Size"]].append(pl)
    for l in lengths:
        if len(lengths[l]) >= 2:
            isolengths.append(lengths[l])

fhw=open('redundancy/redundant_plasmids.tsv','w')
for plist in isolengths:
    tlist = plist.copy()
    while len(tlist) > 1:
        pl1 = tlist.pop(0)
        fh = open('data/'+pl1+'.fna')
        next(fh);seq1=next(fh).strip();fh.close()
        for pl2 in tlist:
            fh = open('data/'+pl2+'.fna')
            next(fh);seq2=next(fh).strip();fh.close()
            seqt=seq2+seq2[0:49]
            last=-1
            while True:
                last = seqt.find(seq1[0:50],last+1)
                if last == -1:
                    break
                if seq1==seq2[last:]+seq2[:last]:
                    break
            if last != -1:
                fhw.write(plasmids[pl1]["pGroup"]+'\t'+pl1+'\t'+pl2+'\n')
                tlist.remove(pl2)
fhw.close()
