#!/usr/bin/env python2

from collections import OrderedDict
from operator import itemgetter
import os
import sys
import argparse


parser = argparse.ArgumentParser(
    description='script for conections')
parser.add_argument('network', nargs='?', type=str, default='Network.csv',
                    help='file with the data about the network edges')
parser.add_argument('nodes', nargs='?', type=str, default='plasmid_mob_70_MOBF.tsv',
                    help='file with the list of nodes')
args = parser.parse_args()

plasmid={}
cluster={}
for taxa in ['species','family','order','class','phylum']:

    if taxa=='species':
        colum=20
    elif taxa=='family':
        colum=18
    elif taxa=='order':
        colum=17
    elif taxa=='class':
        colum=16
    elif taxa=='phylum':
        colum=15

    tabla=open(args.nodes)
    tabla.next()
    especies={} # host sp names and the number of appearances
    ktx_vpl={} # dict of species (as keys) and its list of plasmids AcNum
    kpl_vtx={}  # dict of plasmids (as keys) and the host as value
    for line in tabla:
        linea= line.strip().split('\t')
        especies[linea[colum]] = especies.get(linea[colum], 0) + 1
        if linea[colum] not in ktx_vpl:
            ktx_vpl[linea[colum]]=[]
        ktx_vpl[linea[colum]].append(linea[0])
        kpl_vtx[linea[0]]=linea[colum]
    tabla.close() 
#print ksp_vpl
#print kpl_vsp
    red=open(args.network)
    red.next()
    kpl_vcl={} # dict of plasmids (as keys) and the list of clusters they are linked to
    kcl_vpl={} #dict of clusters (as keys) and the list of plasmids they are linked to
    for line in red:
        linea= line.strip().split('\t')
        if linea[1] not in kpl_vcl:
            kpl_vcl[linea[1]]=[]
        kpl_vcl[linea[1]].append(linea[0])
        if linea[0] not in kcl_vpl:
            kcl_vpl[linea[0]]=[]
        kcl_vpl[linea[0]].append(linea[1])
    red.close()



# FOR THE VIOLINS

    especies_orden=()
    especies_orden= OrderedDict(reversed(sorted(especies.items(), key=itemgetter(1))))

    tra_total={}
    tra_diferentes={}
    diff_host_tra_p={}
    diff_host_tra_p_tx={}

    for k in especies_orden:
    #trajectory measure
        tra_total[k]=0

        tra_diferentes[k]=0

        if (especies[k]>=20) and (k!='-'):
            for p in ktx_vpl[k]:# for each plasmid assigned to a clade(sp).
                if p not in kpl_vcl: #for plasmids without annotated protein, not assigned cluster.The plasmid has no links.
                    continue
                for c in kpl_vcl[p]: # for each cluster that a plasmid is linked to.
                    for plas in kcl_vpl[c]: #for each plasmid that a cluster is linked to.
                        if plas != p:
                            tra_total[k]=tra_total[k]+1 # number of cluster to plasmids links for a given clade
                            if kpl_vtx[plas]!=k: # if the clade of the current(target) plasmid is different of the clade of the start plasmid
                                tra_diferentes[k]=tra_diferentes[k]+1 # links from a plasmids to a other plasmid with different host.
            if tra_total[k]>0:
                diff_host_tra_p[k]=float(tra_diferentes[k])/tra_total[k]
                diff_host_tra_p_tx[k]=(float(tra_diferentes[k])/tra_total[k])/especies[k]

    fv=open('trajectory_'+taxa+'.tsv','w')
    fv.write('Taxa\tDiff_Host_Trajectory_Percentaje\tDiff_Host_Conexion_Trayectory_per_plasmid_unit\n')

    for tx in diff_host_tra_p:
        output = [tx,str(diff_host_tra_p[tx]),str(diff_host_tra_p_tx[tx])]
        fv.write('\t'.join(output) + '\n')

    fv.close()

# GLOBAL_NUMBERS: for the barplots

    cl_diff=0
    cl_tot=0
    for cl in kcl_vpl:
        cltax=[]
        for pl in kcl_vpl[cl]:
            cltax.append(kpl_vtx[pl])
            if '-' in cltax:
                cltax.remove('-')
        if cltax!=[]:
            cl_tot+=1
        if len(set(cltax))>1:
#        print len(cltax), len(set(cltax))
            cl_diff+=1

    cluster[taxa]=float(cl_diff)/cl_tot

    pl_diff=0
    pl_tot=0
    numero=0

    for k in especies:
        if (especies[k]>=20) and (k!='-'):
            numero+=1
            for pl1 in ktx_vpl[k]:# for each plasmid assigned to a clade(sp).
                pl_tot+=1
                pltaxa=[]
                if pl1 in kpl_vcl:
                    for cl in kpl_vcl[pl1]:
                        for pl2 in kcl_vpl[cl]:
                            pltaxa.append(kpl_vtx[pl2])
                if len(set(pltaxa))>1: #more than one taxon connected
                    pl_diff+=1
#    print numero
    plasmid[taxa]=float(pl_diff)/pl_tot

fg=open('conection_globalnumbers.tsv','w')
fg.write('Taxa\tCluster\tPlasmid\n')
for taxa in ['species','family','order','class','phylum']:
    output = [taxa,str(cluster[taxa]),str(plasmid[taxa])]
    fg.write('\t'.join(output) + '\n')

fg.close() 
