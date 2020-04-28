#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import graph_tool.all as gt
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import adjusted_rand_score

def write_classes(filename, graph, state):
    b = state.get_blocks()
    bcc = {}
    for i in np.unique(b.a):
        b_filter = (b.a == i)
        u = gt.GraphView(graph, vfilt=b_filter)
        comp, hist = gt.label_components(u)
        for v in u.vertices():
            bcc[int(v)] = str(i)+'_'+str(comp[v])
    f = open(filename, "w")
    header = "Name\tRealClass\tCComp\tBlockCC\tBlock"
    f.write(header+"\n")
    for v in graph.vertices():
        Name = str(graph.vp.Name[v])
        RealClass = str(graph.vp.RealClass[v])
        CComp = str(graph.vp.CComp[v])
        BlockCC = str(bcc[v])
        Block = str(b[v])
        f.write(Name+"\t"+RealClass+"\t"+CComp+"\t"+BlockCC+"\t"+Block+"\n")
    f.close()

def write_classes_hierarchical(filename, graph, state):
    levels = state.get_levels()
    b = levels[0].get_blocks()
    bcc = {}
    for i in np.unique(b.a):
        b_filter = (b.a == i)
        u = gt.GraphView(graph, vfilt=b_filter)
        comp, hist = gt.label_components(u)
        for v in u.vertices():
            bcc[int(v)] = str(i)+'_'+str(comp[v])
    f = open(filename, "w")
    header = "Name\tRealClass\tCComp\tBlockCC"
    for l in range(len(levels)):
        header = header + "\tBlock" + str(l)
    f.write(header+"\n")
    for v in graph.vertices():
        Name = str(graph.vp.Name[v])
        RealClass = str(graph.vp.RealClass[v])
        CComp = str(graph.vp.CComp[v])
        BlockCC = str(bcc[v])
        Block_list = list()
        r = v
        for l in range(len(levels)):
            r = levels[l].get_blocks()[r]
            Block_list.append(str(r))
        f.write(Name+"\t"+RealClass+"\t"+CComp+"\t"+BlockCC+"\t"+"\t".join(Block_list)+"\n")
    f.close()

def get_blocksCC(graph, blocks):
    v_Bcc = graph.new_vertex_property("string")
    for i in np.unique(blocks.a):
        b_filter = (blocks.a == i)
        u = gt.GraphView(graph, vfilt=b_filter)
        comp, hist = gt.label_components(u)
        for v in u.vertices():
            v_Bcc[v] = str(i)+'_'+str(comp[v])
    return v_Bcc

# Simulate performance on 1000 synthetic networks
# Sample around 2500 items from 300 different classes using a geometric distribution
nIter = 1000
targetClasses = 300
targetItems = 2500
nmi_sbm = []
nmi_nsbm = []
ami_sbm = []
ami_nsbm = []
ar_sbm = []
ar_nsbm = []
for i in range(nIter):
    print("Iteration %d" % i, flush=True)

    pClassSizeShape = 0.3
    pClassSizeScale = 1
    #classSize = np.random.geometric(0.05, size=targetClasses)
    classSize = np.random.gamma(pClassSizeShape, scale=pClassSizeScale, size=targetClasses)
    classSize = np.ceil(classSize * targetItems/np.sum(classSize)).astype(int)
    #classSize[::-1].sort()

    #pickle.dump(classSize, open("sim/sim.pickle", "wb"), -1)
    #classSize = pickle.load(open("sim/sim.pickle", "rb"))

    nVertices = int(sum(classSize))
    print("  Final number of elements: %d" % nVertices, flush=True)
    print("  Detection limit SBM - NSBM: %.3f - %.3f" % (np.sqrt(nVertices), np.log(nVertices)), flush=True)
    print(flush=True)

    #plt.figure()
    #plt.plot(np.sort(classSize)[::-1])
    #plt.savefig('sim/sim_classes_plot.png')
    #plt.close()

    #plt.figure()
    #plt.hist(classSize)
    #plt.savefig('sim/sim_classes_hist.png')
    #plt.close()

    # Assign items their real class
    itemName = np.arange(nVertices)
    className = np.arange(targetClasses)
    itemRealClass = np.empty_like(itemName)
    n = 0
    for cl, s in zip(className, classSize):
        itemRealClass[n:n+s] = cl
        n += s

    # Matrix of per class noise probabilities
    # Diagonal represents the probability for removing intra-group edges: 0 - 0.2 uniform
    # Rest of elements represent the probability for adding inter-group edges: 0 - 0.0001 exponential
    pIntra = 0.2
    pInter = 0.0001
    pClass = np.random.exponential(scale=pInter, size=(targetClasses, targetClasses))
    #np.amax(np.amax(pClass, 1), 0)
    np.fill_diagonal(pClass, np.random.uniform(0, pIntra, size=targetClasses))
    #np.amax(np.diag(pClass), 0)

    # Matrix of possible edge probabilities
    p = np.random.uniform(0, 1, size=(nVertices, nVertices))

    # Create graph
    g = gt.Graph(directed=False)
    g.add_vertex(nVertices)
    v_Name = g.new_vertex_property("int", itemName)
    g.vertex_properties["Name"] = v_Name
    v_RealClass = g.new_vertex_property("int", itemRealClass)
    g.vertex_properties["RealClass"] = v_RealClass
    comp, hist = gt.label_components(g)
    g.vertex_properties["CComp"] = comp

    # Link the items that belong to the same class unless indicated by their class intra-group probability
    # Add noisy edges between elements of different classes with inter-group probability
    elist = []
    vlist = list(g.get_vertices())
    for cl in className:
        vclass = list(np.where(g.vp.RealClass.a == cl)[0])
        for v_o in vclass:
            for v_t in vlist:
                if v_t == v_o:
                    elist.append([v_o, v_t])
                elif v_t in vclass:
                    if p[v_o, v_t] > pClass[cl, cl]:
                        elist.append([v_o, v_t])
                else:
                    if p[v_o, v_t] < pClass[cl, g.vp.RealClass[v_t]]:
                        elist.append([v_o, v_t])
            vlist.remove(v_o)
    g.add_edge_list(elist)

    state = gt.minimize_blockmodel_dl(g, deg_corr=False)
    #write_classes('sim/sim_SBM.tsv', g, state)
    #state.draw(output="sim/sim_SBM.png")
    blocks = state.get_blocks()
    preds = get_blocksCC(g, blocks)
    nmi_sbm.append([normalized_mutual_info_score(g.vp.RealClass.a, blocks.a), normalized_mutual_info_score(g.vp.RealClass.a, list(preds))])
    print("  NMI_SBM = %.5f\tNMI_SBMCC = %.5f" % (nmi_sbm[i][0], nmi_sbm[i][1]), flush=True)
    print("  NMI_SBMavg = %.5f\tNMI_SBMCCavg = %.5f" % (np.mean(np.asarray(nmi_sbm), 0)[0], np.mean(np.asarray(nmi_sbm), 0)[1]), flush=True)
    if i > 2:
        print("  NMI_SBMstd = %.5f\tNMI_SBMCCstd = %.5f" % (np.std(np.asarray(nmi_sbm), 0, ddof=1)[0], np.std(np.asarray(nmi_sbm), 0, ddof=1)[1]), flush=True)
    print(flush=True)
    ami_sbm.append([adjusted_mutual_info_score(g.vp.RealClass.a, blocks.a), adjusted_mutual_info_score(g.vp.RealClass.a, list(preds))])
    print("  AMI_SBM = %.5f\tAMI_SBMCC = %.5f" % (ami_sbm[i][0], ami_sbm[i][1]), flush=True)
    print("  AMI_SBMavg = %.5f\tAMI_SBMCCavg = %.5f" % (np.mean(np.asarray(ami_sbm), 0)[0], np.mean(np.asarray(ami_sbm), 0)[1]), flush=True)
    if i > 2:
        print("  AMI_SBMstd = %.5f\tAMI_SBMCCstd = %.5f" % (np.std(np.asarray(ami_sbm), 0, ddof=1)[0], np.std(np.asarray(ami_sbm), 0, ddof=1)[1]), flush=True)
    print(flush=True)
    ar_sbm.append([adjusted_rand_score(g.vp.RealClass.a, blocks.a), adjusted_rand_score(g.vp.RealClass.a, list(preds))])
    print("  AR_SBM = %.5f\tAR_SBMCC = %.5f" % (ar_sbm[i][0], ar_sbm[i][1]), flush=True)
    print("  AR_SBMavg = %.5f\tAR_SBMCCavg = %.5f" % (np.mean(np.asarray(ar_sbm), 0)[0], np.mean(np.asarray(ar_sbm), 0)[1]), flush=True)
    if i > 2:
        print("  AR_SBMstd = %.5f\tAR_SBMCCstd = %.5f" % (np.std(np.asarray(ar_sbm), 0, ddof=1)[0], np.std(np.asarray(ar_sbm), 0, ddof=1)[1]), flush=True)
    print(flush=True)

    state_nested = gt.minimize_nested_blockmodel_dl(g, deg_corr=False)
    #write_classes_hierarchical('sim/sim_NSBM.tsv', g, state_nested)
    state_nested_l0 = state_nested.get_levels()[0]
    #state_nested_l0.draw(output="sim/sim_NSBM.png")
    blocks_n = state_nested_l0.get_blocks()
    preds_n = get_blocksCC(g, blocks_n)
    nmi_nsbm.append([normalized_mutual_info_score(g.vp.RealClass.a, blocks_n.a), normalized_mutual_info_score(g.vp.RealClass.a, list(preds_n))])
    print("  NMI_NSBM = %.5f\tNMI_NSBMCC = %.5f" % (nmi_nsbm[i][0], nmi_nsbm[i][1]), flush=True)
    print("  NMI_NSBMavg = %.5f\tNMI_NSBMCCavg = %.5f" % (np.mean(np.asarray(nmi_nsbm), 0)[0], np.mean(np.asarray(nmi_nsbm), 0)[1]), flush=True)
    if i > 2:
        print("  NMI_NSBMstd = %.5f\tNMI_NSBMCCstd = %.5f" % (np.std(np.asarray(nmi_nsbm), 0, ddof=1)[0], np.std(np.asarray(nmi_nsbm), 0, ddof=1)[1]), flush=True)
    print(flush=True)
    ami_nsbm.append([adjusted_mutual_info_score(g.vp.RealClass.a, blocks_n.a), adjusted_mutual_info_score(g.vp.RealClass.a, list(preds_n))])
    print("  AMI_NSBM = %.5f\tAMI_NSBMCC = %.5f" % (ami_nsbm[i][0], ami_nsbm[i][1]), flush=True)
    print("  AMI_NSBMavg = %.5f\tAMI_NSBMCCavg = %.5f" % (np.mean(np.asarray(ami_nsbm), 0)[0], np.mean(np.asarray(ami_nsbm), 0)[1]), flush=True)
    if i > 2:
        print("  AMI_NSBMstd = %.5f\tAMI_NSBMCCstd = %.5f" % (np.std(np.asarray(ami_nsbm), 0, ddof=1)[0], np.std(np.asarray(ami_nsbm), 0, ddof=1)[1]), flush=True)
    print(flush=True)
    ar_nsbm.append([adjusted_rand_score(g.vp.RealClass.a, blocks_n.a), adjusted_rand_score(g.vp.RealClass.a, list(preds_n))])
    print("  AR_NSBM = %.5f\tAR_NSBMCC = %.5f" % (ar_nsbm[i][0], ar_nsbm[i][1]), flush=True)
    print("  AR_NSBMavg = %.5f\tAR_NSBMCCavg = %.5f" % (np.mean(np.asarray(ar_nsbm), 0)[0], np.mean(np.asarray(ar_nsbm), 0)[1]), flush=True)
    if i > 2:
        print("  AR_NSBMstd = %.5f\tAR_NSBMCCstd = %.5f" % (np.std(np.asarray(ar_nsbm), 0, ddof=1)[0], np.std(np.asarray(ar_nsbm), 0, ddof=1)[1]), flush=True)
    print(flush=True)

pickle.dump(nmi_sbm, nmi_nsbm, ami_sbm, ami_nsbm, ar_sbm, ar_nsbm, open("sim/sim_bootstrap.pickle", "wb"), -1)

print("NMI_SBMavg = %.5f\tNMI_SBMCCavg = %.5f" % (np.mean(np.asarray(nmi_sbm), 0)[0], np.mean(np.asarray(nmi_sbm), 0)[1]))
print("NMI_SBMstd = %.5f\tNMI_SBMCCstd = %.5f" % (np.std(np.asarray(nmi_sbm), 0, ddof=1)[0], np.std(np.asarray(nmi_sbm), 0, ddof=1)[1]))
print()
print("NMI_NSBMavg = %.5f\tNMI_NSBMCCavg = %.5f" % (np.mean(np.asarray(nmi_nsbm), 0)[0], np.mean(np.asarray(nmi_nsbm), 0)[1]))
print("NMI_NSBMstd = %.5f\tNMI_NSBMCCstd = %.5f" % (np.std(np.asarray(nmi_nsbm), 0, ddof=1)[0], np.std(np.asarray(nmi_nsbm), 0, ddof=1)[1]))
print()
print("AMI_SBMavg = %.5f\tAMI_SBMCCavg = %.5f" % (np.mean(np.asarray(ami_sbm), 0)[0], np.mean(np.asarray(ami_sbm), 0)[1]))
print("AMI_SBMstd = %.5f\tAMI_SBMCCstd = %.5f" % (np.std(np.asarray(ami_sbm), 0, ddof=1)[0], np.std(np.asarray(ami_sbm), 0, ddof=1)[1]))
print()
print("AMI_NSBMavg = %.5f\tAMI_NSBMCCavg = %.5f" % (np.mean(np.asarray(ami_nsbm), 0)[0], np.mean(np.asarray(ami_nsbm), 0)[1]))
print("AMI_NSBMstd = %.5f\tAMI_NSBMCCstd = %.5f" % (np.std(np.asarray(ami_nsbm), 0, ddof=1)[0], np.std(np.asarray(ami_nsbm), 0, ddof=1)[1]))
print()
print("AR_SBMavg = %.5f\tAR_SBMCCavg = %.5f" % (np.mean(np.asarray(ar_sbm), 0)[0], np.mean(np.asarray(ar_sbm), 0)[1]))
print("AR_SBMstd = %.5f\tAR_SBMCCstd = %.5f" % (np.std(np.asarray(ar_sbm), 0, ddof=1)[0], np.std(np.asarray(ar_sbm), 0, ddof=1)[1]))
print()
print("AR_NSBMavg = %.5f\tAR_NSBMCCavg = %.5f" % (np.mean(np.asarray(ar_nsbm), 0)[0], np.mean(np.asarray(ar_nsbm), 0)[1]))
print("AR_NSBMstd = %.5f\tAR_NSBMCCstd = %.5f" % (np.std(np.asarray(ar_nsbm), 0, ddof=1)[0], np.std(np.asarray(ar_nsbm), 0, ddof=1)[1]))
