#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd
import graph_tool.all as gt
import matplotlib.pyplot as plt
from sklearn.metrics import log_loss
from sklearn.metrics import f1_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import homogeneity_score
from sklearn.metrics import completeness_score
from sklearn.metrics import v_measure_score

nodes = pd.read_csv("plasmid_mob_pfinder_PTU.tsv", sep="\t")
nodes.columns

nodesf = nodes[nodes.Filtered == "No"]
nodesfe = nodesf[nodesf.TaxOrder == "Enterobacterales"]
nodesfn = nodesf[nodesf.TaxOrder != "Enterobacterales"]

unique, counts = np.unique(nodesf.CComp, return_counts=True)
nodesf4 = nodesf[np.isin(nodesf.CComp, unique[counts >= 4])]
nodesf4e = nodesf4[nodesf4.TaxOrder == "Enterobacterales"]
nodesf4n = nodesf4[nodesf4.TaxOrder != "Enterobacterales"]

print(adjusted_rand_score(nodesf.PTU_Manual, nodesf.PTU_PID), \
      adjusted_mutual_info_score(nodesf.PTU_Manual, nodesf.PTU_PID), \
      normalized_mutual_info_score(nodesf.PTU_Manual, nodesf.PTU_PID), sep="\t")
print(adjusted_rand_score(nodesf.PTU_Manual, nodesf.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf.PTU_Manual, nodesf.PTU_NSBM), \
      normalized_mutual_info_score(nodesf.PTU_Manual, nodesf.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf.PTU_PID, nodesf.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf.PTU_PID, nodesf.PTU_NSBM), \
      normalized_mutual_info_score(nodesf.PTU_PID, nodesf.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf.SubGraphPID, nodesf.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf.SubGraphPID, nodesf.PTU_NSBM), \
      normalized_mutual_info_score(nodesf.SubGraphPID, nodesf.PTU_NSBM), sep="\t")
#0.9124827425758636	0.9284656565609233	0.940573225303294
#0.6483817484867183	0.7602577272905321	0.8086615562196372
#0.6087368362471499	0.7290172312147002	0.7830220239342065
#0.7157891340383642	0.7905621821870875	0.8353238971873171

print(adjusted_rand_score(nodesfe.PTU_Manual, nodesfe.PTU_PID), \
      adjusted_mutual_info_score(nodesfe.PTU_Manual, nodesfe.PTU_PID), \
      normalized_mutual_info_score(nodesfe.PTU_Manual, nodesfe.PTU_PID), sep="\t")
print(adjusted_rand_score(nodesfe.PTU_Manual, nodesfe.PTU_NSBM), \
      adjusted_mutual_info_score(nodesfe.PTU_Manual, nodesfe.PTU_NSBM), \
      normalized_mutual_info_score(nodesfe.PTU_Manual, nodesfe.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesfe.PTU_PID, nodesfe.PTU_NSBM), \
      adjusted_mutual_info_score(nodesfe.PTU_PID, nodesfe.PTU_NSBM), \
      normalized_mutual_info_score(nodesfe.PTU_PID, nodesfe.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesfe.SubGraphPID, nodesfe.PTU_NSBM), \
      adjusted_mutual_info_score(nodesfe.SubGraphPID, nodesfe.PTU_NSBM), \
      normalized_mutual_info_score(nodesfe.SubGraphPID, nodesfe.PTU_NSBM), sep="\t")
#0.6253260007696984	0.8274708392193632	0.8570951201232417
#0.6391293492462684	0.8428542913774173	0.8739753276481949
#0.4797592956529133	0.7663804836981944	0.8116529932911478
#0.4797592956529133	0.7663804836981939	0.8116529932911478

print(adjusted_rand_score(nodesfn.PTU_Manual, nodesfn.PTU_PID), \
      adjusted_mutual_info_score(nodesfn.PTU_Manual, nodesfn.PTU_PID), \
      normalized_mutual_info_score(nodesfn.PTU_Manual, nodesfn.PTU_PID), sep="\t")
print(adjusted_rand_score(nodesfn.PTU_Manual, nodesfn.PTU_NSBM), \
      adjusted_mutual_info_score(nodesfn.PTU_Manual, nodesfn.PTU_NSBM), \
      normalized_mutual_info_score(nodesfn.PTU_Manual, nodesfn.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesfn.PTU_PID, nodesfn.PTU_NSBM), \
      adjusted_mutual_info_score(nodesfn.PTU_PID, nodesfn.PTU_NSBM), \
      normalized_mutual_info_score(nodesfn.PTU_PID, nodesfn.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesfn.SubGraphPID, nodesfn.PTU_NSBM), \
      adjusted_mutual_info_score(nodesfn.SubGraphPID, nodesfn.PTU_NSBM), \
      normalized_mutual_info_score(nodesfn.SubGraphPID, nodesfn.PTU_NSBM), sep="\t")
#0.9991959596856393	0.9990760265477908	0.9992052631914119
#0.6091047788911677	0.7089895193663522	0.758606347323617
#0.6091042951811059	0.708889546752521	0.7585440241216577
#0.7670714214355874	0.8054995272300922	0.8424151741726013

print(adjusted_rand_score(nodesf4.PTU_Manual, nodesf4.PTU_PID), \
      adjusted_mutual_info_score(nodesf4.PTU_Manual, nodesf4.PTU_PID), \
      normalized_mutual_info_score(nodesf4.PTU_Manual, nodesf4.PTU_PID), sep="\t")
print(adjusted_rand_score(nodesf4.PTU_Manual, nodesf4.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4.PTU_Manual, nodesf4.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4.PTU_Manual, nodesf4.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf4.PTU_PID, nodesf4.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4.PTU_PID, nodesf4.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4.PTU_PID, nodesf4.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf4.SubGraphPID, nodesf4.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4.SubGraphPID, nodesf4.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4.SubGraphPID, nodesf4.PTU_NSBM), sep="\t")
#0.8347334872491533	0.9195195401470017	0.9413092014427025
#0.26431779856290133	0.7311102666773487	0.8194514703131016
#0.22823438930195492	0.6947568636233841	0.7938355943628516
#0.3359911689061147	0.7578345466790424	0.8423297470670562

print(adjusted_rand_score(nodesf4e.PTU_Manual, nodesf4e.PTU_PID), \
      adjusted_mutual_info_score(nodesf4e.PTU_Manual, nodesf4e.PTU_PID), \
      normalized_mutual_info_score(nodesf4e.PTU_Manual, nodesf4e.PTU_PID), sep="\t")
print(adjusted_rand_score(nodesf4e.PTU_Manual, nodesf4e.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4e.PTU_Manual, nodesf4e.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4e.PTU_Manual, nodesf4e.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf4e.PTU_PID, nodesf4e.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4e.PTU_PID, nodesf4e.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4e.PTU_PID, nodesf4e.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf4e.SubGraphPID, nodesf4e.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4e.SubGraphPID, nodesf4e.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4e.SubGraphPID, nodesf4e.PTU_NSBM), sep="\t")
#0.5206401390334028	0.82688302688457	0.8604248544695738
#0.5576096083222645	0.8436801847755518	0.8789314204131392
#0.34736636599067217	0.7656850576489178	0.8172294752049748
#0.34736636599067217	0.7656850576489176	0.8172294752049748

print(adjusted_rand_score(nodesf4n.PTU_Manual, nodesf4n.PTU_PID), \
      adjusted_mutual_info_score(nodesf4n.PTU_Manual, nodesf4n.PTU_PID), \
      normalized_mutual_info_score(nodesf4n.PTU_Manual, nodesf4n.PTU_PID), sep="\t")
print(adjusted_rand_score(nodesf4n.PTU_Manual, nodesf4n.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4n.PTU_Manual, nodesf4n.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4n.PTU_Manual, nodesf4n.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf4n.PTU_PID, nodesf4n.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4n.PTU_PID, nodesf4n.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4n.PTU_PID, nodesf4n.PTU_NSBM), sep="\t")
print(adjusted_rand_score(nodesf4n.SubGraphPID, nodesf4n.PTU_NSBM), \
      adjusted_mutual_info_score(nodesf4n.SubGraphPID, nodesf4n.PTU_NSBM), \
      normalized_mutual_info_score(nodesf4n.SubGraphPID, nodesf4n.PTU_NSBM), sep="\t")
#0.998529406078652	0.9988969905823087	0.9991870678387716
#0.2166843066712238	0.6629112604948727	0.7732711059943755
#0.21667808563620222	0.66272941357295	0.7731971039964834
#0.3860418806328456	0.762680345161316	0.8493041323508992

for i in np.unique(nodesfe.PTU_NSBM):
    tmp=nodesfe[nodesfe.PTU_NSBM==i]
    unique, counts = np.unique(tmp.PTU_Manual, return_counts=True)
    l = []
    for n, u in enumerate(unique):
        l.append((u, counts[n], len(nodesf4e[nodesf4e.PTU_NSBM == u]))
    print(i, len(tmp), l, sep="\t")

t = 'PTU_Manual'
r1 = 'PTU_PID'
r2 = 'PTU_NSBM'
for i in np.unique(nodesf4e[t]):
    tmp = nodesf4e[nodesf4e[t] == i]
    unique1, counts1 = np.unique(tmp[r1], return_counts=True)
    list1 = []
    for n, u in enumerate(unique1):
        list1.append((u, counts1[n], len(nodesf4e[nodesf4e[r1] == u]), counts1[n]/len(tmp), \
                      len(nodesf4e[nodesf4e[r1] == u])/len(tmp) if (len(tmp) > len(nodesf4e[nodesf4e[r1] == u])) else len(tmp)/len(nodesf4e[nodesf4e[r1] == u])))
    unique2, counts2 = np.unique(tmp[r2], return_counts=True)
    list2 = []
    for n, u in enumerate(unique2):
        list2.append((u, counts2[n], len(nodesf4e[nodesf4e[r2] == u]), counts2[n]/len(tmp), \
                      len(nodesf4e[nodesf4e[r2] == u])/len(tmp) if (len(tmp) > len(nodesf4e[nodesf4e[r2] == u])) else len(tmp)/len(nodesf4e[nodesf4e[r2] == u])))
    print(i, len(tmp), list1, sep="\t")
    print('', '', list2, sep="\t")
