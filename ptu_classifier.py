#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import graph_tool.all as gt
from sklearn.metrics import log_loss
from sklearn.metrics import f1_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import homogeneity_score
from sklearn.metrics import completeness_score
from sklearn.metrics import v_measure_score

#outdir = "final_results_kept_NSBM_wAL-nDC"
#if not os.path.exists(outdir): os.mkdir(outdir)

# Load ANI matrix and metadata
ani_fname = "/fernando/data/Plasmid_Chart/adjacency/matrix_ANIp50_kept.tsv"
#ani_fname = "/fernando/data/Plasmid_Chart/adjacency/matrix_ANIp50_Ent.tsv"
nodes_fname = "/fernando/data/Plasmid_Chart/auto_pTUs/update_assignment/nodes_kept.tsv"
#nodes_fname = "/fernando/data/Plasmid_Chart/auto_pTUs/update_assignment/nodes_Ent.tsv"

nodes = pd.read_csv(nodes_fname, sep="\t")
ani = pd.read_csv(ani_fname, sep="\t", header=None, names=nodes.AccessionVersion)

# Graph vertices number
nVertices = ani.shape[0]

# Create undirected graph
g = gt.Graph(directed=False)
g.add_vertex(nVertices)

# Use the ANI matrix to define the graph topology
ani_np = ani.to_numpy() # Complete ANI matrix (symetric, with autoloops)
ani_np = np.triu(ani.to_numpy(), 0) # Upper triangular ANI matrix (with autoloops)
ani_np_idx = ani_np.nonzero()
g.add_edge_list(np.transpose(ani_np_idx))

# Use ANI as edge weights
e_ANI = g.new_edge_property("double")
e_ANI.a = ani_np[ani_np_idx] / 100
g.edge_properties["ANI"] = e_ANI

# Use AccessionVersion to name the vertices
v_AccVer = g.new_vertex_property("string", nodes.AccessionVersion.to_list())
g.vertex_properties["AccessionVersion"] = v_AccVer

# Add other relevant properties to vertices
v_MOB = g.new_vertex_property("string", nodes.MOB_60.to_list())
g.vertex_properties["MOB"] = v_MOB
v_PFinder = g.new_vertex_property("string", nodes.PFinder_80.to_list())
g.vertex_properties["PFinder"] = v_PFinder
v_Size = g.new_vertex_property("int", nodes.Size.to_list())
g.vertex_properties["Size"] = v_Size
v_PtuManual = g.new_vertex_property("string", nodes.PTU_ManPID_200213.to_list())
g.vertex_properties["PtuManual"] = v_PtuManual
#g.list_properties()

# Filter out connected components with less than 4 members
#comp, hist = gt.label_components(g)
#g.vertex_properties["CComp"] = comp
#v_CC4 = g.new_vertex_property("bool", np.isin(comp.a, np.where(hist >= 4)))
#g.vertex_properties["CC4_filter"] = v_CC4
#g.set_vertex_filter(g.vp.CC4_filter)
#g.purge_vertices()
#g.set_vertex_filter(None)
fname = "ani_l50_graph"
g.save(os.path.join(outdir,fname+".gt.gz"))
nVertFilt = g.num_vertices()

def ptu_annotation(graph, state):
    levels = state.get_levels()

    levels_nr = []
    save_flag = True
    for l in reversed(range(1, len(levels))):
        b_o = state.project_partition(l, 0).a
        b_t = state.project_partition(l-1, 0).a
        if (save_flag == True):
            levels_nr.append(l)
            if (adjusted_mutual_info_score(b_o, b_t) >= 1):
                save_flag = False
        else:
            if (adjusted_mutual_info_score(b_o, b_t) < 1):
                save_flag = True
    if (save_flag == True):
        levels_nr.append(0)

    b = levels[0].get_blocks()
    bcc = {}
    bcc4 = {}
    for i in np.unique(b.a):
        b_filter = (b.a == i)
        u = gt.GraphView(graph, vfilt=b_filter)
        tmp = []
        r = u.get_vertices()[0]
        for l in range(len(levels)):
            r = levels[l].get_blocks()[r]
            if l in levels_nr:
                tmp.append(str(r))
        tmp.reverse()
        comp, hist = gt.label_components(u)
        for v in u.vertices():
            tag = '_'.join(tmp+[str(comp[v])])
            bcc[int(v)] = tag
            bcc4[int(v)] = tag if (hist[comp[int(v)]] >= 4) else '-'

    return((bcc, bcc4))

def ptucomplex_annotation(graph):
    complex = []
    bcc4 = list(graph.vp.BlockCC4)
    bcc4_nr = np.unique(bcc4)
    common_levels = 7
    #f=open('pru.tsv', 'w')
    for n, i in enumerate(bcc4_nr[:-1]):
        if i == '-':
            continue
        i_filter = (np.array(bcc4) == i)
        u = gt.GraphView(graph, vfilt=i_filter)
        u_vertices = u.num_vertices()
        u_edges = u.num_edges()
        u_size = {'med': np.median(list(u.vp.Size))}
        #u_size['avg'], u_size['std'] = gt.vertex_average(u, u.vp.Size)
        unique, counts = np.unique(list(u.vp.PtuManual), return_counts=True)
        if (unique[counts.argmax()] == '-'):
            if len(unique) == 1:
                u_ptu = '-'
            else:
                tmp = np.delete(np.array(list(u.vp.PtuManual)), np.argwhere(np.array(list(u.vp.PtuManual)) == '-'))
                unique, counts = np.unique(tmp, return_counts=True)
                u_ptu = unique[counts.argmax()]
        else:
            u_ptu = unique[counts.argmax()]
        unique, counts = np.unique(list(u.vp.MOB), return_counts=True)
        if (unique[counts.argmax()] == '-'):
            if len(unique) == 1:
                u_mob = '-'
                u_mob_freq = '_'.join((str(counts[counts.argmax()]), str(u_vertices)))
            else:
                tmp = np.delete(np.array(list(u.vp.MOB)), np.argwhere(np.array(list(u.vp.MOB)) == '-'))
                unique, counts = np.unique(tmp, return_counts=True)
                u_mob = unique[counts.argmax()]
                u_mob_freq = '_'.join((str(counts[counts.argmax()]), str(u_vertices)))
        else:
            u_mob = unique[counts.argmax()]
            u_mob_freq = '_'.join((str(counts[counts.argmax()]), str(u_vertices)))
        for j in bcc4_nr[n+1:]:
            if (j == '-'):
                continue
            if ('_'.join(j.split('_')[:common_levels]) != '_'.join(i.split('_')[:common_levels])):
                continue
            j_filter = (np.array(bcc4) == j)
            w = gt.GraphView(graph, vfilt=j_filter)
            w_vertices = w.num_vertices()
            w_edges = w.num_edges()
            w_size = {'med': np.median(list(w.vp.Size))}
            #w_size['avg'], w_size['std'] = gt.vertex_average(w, w.vp.Size)
            unique, counts = np.unique(list(w.vp.PtuManual), return_counts=True)
            if (unique[counts.argmax()] == '-'):
                if len(unique) == 1:
                    w_ptu = '-'
                else:
                    tmp = np.delete(np.array(list(w.vp.PtuManual)), np.argwhere(np.array(list(w.vp.PtuManual)) == '-'))
                    unique, counts = np.unique(tmp, return_counts=True)
                    w_ptu = unique[counts.argmax()]
            else:
                w_ptu = unique[counts.argmax()]
            unique, counts = np.unique(list(w.vp.MOB), return_counts=True)
            if (unique[counts.argmax()] == '-'):
                if len(unique) == 1:
                    w_mob = '-'
                    w_mob_freq = '_'.join((str(counts[counts.argmax()]), str(w_vertices)))
                else:
                    tmp = np.delete(np.array(list(w.vp.MOB)), np.argwhere(np.array(list(w.vp.MOB)) == '-'))
                    unique, counts = np.unique(tmp, return_counts=True)
                    w_mob = unique[counts.argmax()]
                    w_mob_freq = '_'.join((str(counts[counts.argmax()]), str(w_vertices)))
            else:
                w_mob = unique[counts.argmax()]
                w_mob_freq = '_'.join((str(counts[counts.argmax()]), str(w_vertices)))
            #u_comp = True if (abs(u_size['med'] - w_size['med']) < (u_size['med'] * 0.5)) else False
            #w_comp = True if (abs(u_size['med'] - w_size['med']) < (w_size['med'] * 0.5)) else False
            if (u_size['med'] > w_size['med']):
                s_comp = True if (abs(u_size['med'] - w_size['med']) < (u_size['med'] * 0.5)) else False
            else:
                s_comp = True if (abs(u_size['med'] - w_size['med']) < (w_size['med'] * 0.5)) else False
            k_filter = np.logical_or(i_filter, j_filter)
            z = gt.GraphView(graph, vfilt=k_filter)
            z_vertices = z.num_vertices()
            z_edges = z.num_edges()
            #z_comp_1 = True if (z_edges > (u_edges + w_edges)) else False
            z_comp_p = True if (z_edges - (u_edges + w_edges) > (u_vertices * w_vertices*((u_edges-u_vertices)/(u_vertices*(u_vertices-1)/2))*((w_edges-w_vertices)/(w_vertices*(w_vertices-1)/2))*0.5)) else False
            if z_comp_p and s_comp and ((u_mob == w_mob) or (u_mob == '-') or (w_mob == '-')):
                for m, c in enumerate(complex):
                    if (i in c) or (j in c):
                        if i not in c:
                            complex[m].append(i)
                        if j not in c:
                            complex[m].append(j)
                        break
                else:
                    complex.append([i, j])
                for m, c in enumerate(complex[:-1]):
                    for l, d in enumerate(complex[m+1:]):
                        for e in c:
                            if e in d:
                                complex[m] = complex[m] + list(set(d) - set(c))
                                complex.pop(l+m+1)
                                break
            #if z_comp_1 and (u_comp or w_comp):
            #    f.write("\t".join((i, j, u_ptu, w_ptu, \
            #                       str(u_size['med']), str(w_size['med']), str(abs(u_size['med'] - w_size['med'])), \
            #                       str(u_comp), str(w_comp), \
            #                       u_mob, u_mob_freq, w_mob, w_mob_freq)) + '\n')
    #for m, c in enumerate(complex):
    #    f.write('\n')
    #    for l, e in enumerate(c):
    #        e_filter = (np.array(bcc4) == e)
    #        u = gt.GraphView(graph, vfilt=e_filter)
    #        unique, counts = np.unique(list(u.vp.PtuManual), return_counts=True)
    #        complex[m][l] = e + '-' + unique[counts.argmax()]
    #        f.write(complex[m][l]+'\t')
    #f.close()
    cmplx = {}
    for i in bcc4_nr:
        for m, c in enumerate(complex):
            if i in c:
                cmplx[i] = c[0]
                break
        else:
            cmplx[i] = i
    v_Complex = graph.new_vertex_property("string")
    for v in graph.vertices():
        v_Complex[v] = cmplx[graph.vp.BlockCC4[v]]
    cpl={}
    for i in np.unique(list(v_Complex)):
        if i == '-':
            cpl[i] = '-'
            continue
        i_filter = (np.array(list(v_Complex)) == i)
        u = gt.GraphView(graph, vfilt=i_filter)
        unique, counts = np.unique(list(u.vp.PtuManual), return_counts=True)
        if (unique[counts.argmax()] == '-'):
            if len(unique) == 1:
                cpl[i] = '-'
            else:
                tmp = np.delete(np.array(list(u.vp.PtuManual)), np.argwhere(np.array(list(u.vp.PtuManual)) == '-'))
                unique, counts = np.unique(tmp, return_counts=True)
                cpl[i] = unique[counts.argmax()]
        else:
            cpl[i] = unique[counts.argmax()]

    #f=open('NSBM_kept_200404_PtuSBM_to_PTU.tsv','w')
    #for i in cpl:
    #    f.write(i+'\t'+cpl[i]+'\n')
    #f.close()
    #f=open('NSBM_kept_200404_PtuSBM.tsv','w')
    #for v in graph.vertices():
    #    f.write('\t'.join((graph.vp.AccessionVersion[v],graph.vp.PtuManual[v],str(graph.vp.CComp[v]),graph.vp.BlockCC[v],graph.vp.BlockCC4[v],v_Complex[v]))+'\n')
    #f.close()

    return(v_Complex)

def write_classes(filename, graph):
    f = open(filename, "w")
    if 'BlockCC' in g.vp.keys():
        header = "AccessionVersion\tPtuManual\tCComp\tBlockCC\tBlockCC4"
    else:
        header = "AccessionVersion\tPtuManual\tCComp"
    f.write(header+"\n")
    for v in graph.vertices():
        AccVer = graph.vp.AccessionVersion[v]
        PtuManual = graph.vp.PtuManual[v]
        CComp = str(graph.vp.CComp[v])
        if 'BlockCC' in g.vp.keys():
            BlockCC = graph.vp.BlockCC[v]
            BlockCC4 = graph.vp.BlockCC4[4]
            f.write("\t".join((AccVer, PtuManual, CComp, BlockCC, BlockCC4)) + "\n")
        else:
            f.write("\t".join((AccVer, PtuManual, CComp)) +"\n")
    f.close()

nToss = 100
state_list, entropy_list = [], []
for k in range(nToss):
    # Nested stochastic block model (hierarchical SBM)
    state = gt.minimize_nested_blockmodel_dl(g, deg_corr=False)
    state_0 = state.get_levels()[0]
    entropy = state.entropy()

    # Update state
    state_list.append(state)
    entropy_list.append(entropy)
    nClass = len(np.unique(state_0.get_blocks().a))
    print("Toss %d of %d: %d classes, entropy %f" % (k, nToss, nClass, entropy))

    # Save graph
    fname = "NSBM_%d_%f" % (nClass, entropy)
    write_classes(os.path.join(outdir,fname+".tsv"), g, state)
    pickle.dump([g, state], open(os.path.join(outdir,fname+".pickle"), "wb"), -1)
    #g.save(os.path.join(outdir,fname+".gt.gz"))
k = np.argmin(entropy_list)
state, entropy = state_list[k], entropy_list[k]
bs = state.get_bs()
bs += [np.zeros(1)] * (15 - len(bs))
state = state.copy(bs=bs, sampling=True)
state_0 = state.get_levels()[0]
nClass = len(np.unique(state_0.get_blocks().a))
print("Selected toss %d: %d classes, entropy %f" % (k, nClass, entropy))

# Avoid the transient state
gt.mcmc_equilibrate(state, wait=4000, nbreaks=2, multiflip=True, mcmc_args=dict(niter=10), verbose=False)
entropy = state.entropy()
state_0 = state.get_levels()[0]
nClass = len(np.unique(state_0.get_blocks().a))
print("%d classes, entropy %f" % (nClass, entropy))

(bcc, bcc4) = ptu_annotation(g, state)
v_BlockCC = g.new_vertex_property("string")
v_BlockCC4 = g.new_vertex_property("string")
for v in g.vertices():
    v_BlockCC[v] = bcc[int(v)]
    v_BlockCC4[v] = bcc4[int(v)]
g.vertex_properties["BlockCC"] = v_BlockCC
g.vertex_properties["BlockCC4"] = v_BlockCC4

# Save graph
fname = "NSBM_mcmc_ini_%d_%f" % (nClass, entropy)
write_classes(os.path.join(outdir,fname+".tsv"), g, state)
pickle.dump([g, state], open(os.path.join(outdir,fname+".pickle"), "wb"), -1)
#g.save(os.path.join(outdir,fname+".gt.gz"))

# Callback to collect the vertex marginal probabilities
dls = [] # Description length history
pv = [None] * len(state.get_levels()) # Vertex marginals
pe = None # Edge marginals
def collect_marginals(s):
    global pv, pe
    levels = s.get_levels()
    pv = [sl.collect_vertex_marginals(pv[l], b=gt.perfect_prop_hash([sl.b])[0]) for l, sl in enumerate(levels)]
    pe = levels[0].collect_edge_marginals(pe)
    dls.append(s.entropy())

# Apply MCMC
gt.mcmc_equilibrate(state, force_niter=20000, mcmc_args=dict(niter=10), callback=collect_marginals)
entropy = state.entropy()
S_mf = [gt.mf_entropy(sl.g, pv[l]) for l, sl in enumerate(state.get_levels())]
S_bethe = gt.bethe_entropy(g, pe)[0]
L = -np.mean(dls)
state_0 = state.get_levels()[0]
nClass = len(np.unique(state_0.get_blocks().a))
print("%d classes, entropy %f, mean_field %f, bethe %f" % (nClass, entropy, L+sum(S_mf), L+S_bethe+sum(S_mf[1:])))

(bcc, bcc4) = ptu_annotation(g, state)
v_BlockCC = g.new_vertex_property("string")
v_BlockCC4 = g.new_vertex_property("string")
for v in g.vertices():
    v_BlockCC[v] = bcc[int(v)]
    v_BlockCC4[v] = bcc4[int(v)]
g.vertex_properties["BlockCC"] = v_BlockCC
g.vertex_properties["BlockCC4"] = v_BlockCC4

v_Complex = ptucomplex_annotation(g)
g.vertex_properties["Complex"] = v_Complex

# Save final graph
fname = "NSBM_mcmc_%d_%f" % (nClass, entropy)
write_classes(os.path.join(outdir,fname+".tsv"), g, state)
pickle.dump([g, state, dls, pv, pe, S_mf, S_bethe], open(os.path.join(outdir,fname+".pickle"), "wb"), -1)
#g.save(os.path.join(outdir,fname+".gt.gz"))

#with open('final_models/results_kept_NSBM_wAL-nDC/NSBM_mcmc_534_159837.233284.pickle', 'rb') as f:
#    [g, state, dls, pv, pe, S_mf, S_bethe] = pickle.load(f)
#for v in g.vertices():
#    g.vp.Size[v] = nodes.Size[nodes.AccessionVersion == g.vp.AccessionVersion[v]]

# Draw final state
#state.draw(os.path.join(outdir,fname+".png"))
#state.draw(os.path.join(outdir,fname+".svg"))

# Find the maximal nClass over all mcmc sweeps
nClassMax = 0
for v in g.vertices():
    nClassMax = max(nClassMax, len(pv[0][v]))

# Build the probability matrix (nVertFilt x nClassMax)
# This matrix is stochastic by rows
P = np.zeros([nVertFilt, nClassMax])
# Each node has some probability to belong to each class
for i, v in enumerate(g.vertices()):
    p = np.array(pv[0][v]) / sum(pv[0][v])
    for j in range(len(p)):
        P[i, j] = p[j]
fname = "NSBM_P_%d-%d_%f.tsv" % (nClass, nClassMax, entropy)
np.savetxt(os.path.join(outdir,fname), P)

