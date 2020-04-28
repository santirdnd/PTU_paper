#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import graph_tool.all as gt

outdir = "results_kept_NSBM_wAL-nDC"
if not os.path.exists(outdir): os.mkdir(outdir)

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
v_PtuManual = g.new_vertex_property("string", nodes.PTU_ManPID_200213.to_list())
g.vertex_properties["PtuManual"] = v_PtuManual
#g.list_properties()

# Filter out connected components with less than 4 members
comp, hist = gt.label_components(g)
g.vertex_properties["CComp"] = comp
v_CC4 = g.new_vertex_property("bool", np.isin(comp.a, np.where(hist >= 4)))
g.vertex_properties["CC4_filter"] = v_CC4
g.set_vertex_filter(g.vp.CC4_filter)
g.purge_vertices()
g.set_vertex_filter(None)
fname = "NSBM"
g.save(os.path.join(outdir,fname+".gt.gz"))
nVertFilt = g.num_vertices()

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
    header = "AccessionVersion\tPTU\tCComp\tBlockCC"
    for l in range(len(levels)):
        header = header + "\tBlock" + str(l)
    f.write(header+"\n")
    for v in graph.vertices():
        AccVer = graph.vp.AccessionVersion[v]
        PtuManual = graph.vp.PtuManual[v]
        CComp = str(graph.vp.CComp[v])
        BlockCC = bcc[v]
        Block_list = list()
        r = v
        for l in range(len(levels)):
            r = levels[l].get_blocks()[r] # The tutorial seems to be wrong here
            Block_list.append(str(r))
        f.write(AccVer+"\t"+PtuManual+"\t"+CComp+"\t"+BlockCC+"\t"+"\t".join(Block_list)+"\n")
    f.close()

# Find the initial model with minimum entropy
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
    write_classes_hierarchical(os.path.join(outdir,fname+".tsv"), g, state)
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
gt.mcmc_equilibrate(state, wait=2000, nbreaks=2, multiflip=True, mcmc_args=dict(niter=10), verbose=False)
entropy = state.entropy()
state_0 = state.get_levels()[0]
nClass = len(np.unique(state_0.get_blocks().a))
print("%d classes, entropy %f" % (nClass, entropy))

# Save graph
fname = "NSBM_mcmc_ini_%d_%f" % (nClass, entropy)
write_classes_hierarchical(os.path.join(outdir,fname+".tsv"), g, state)
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
gt.mcmc_equilibrate(state, force_niter=10000, mcmc_args=dict(niter=10), callback=collect_marginals)
entropy = state.entropy()
S_mf = [gt.mf_entropy(sl.g, pv[l]) for l, sl in enumerate(state.get_levels())]
S_bethe = gt.bethe_entropy(g, pe)[0]
L = -np.mean(dls)
state_0 = state.get_levels()[0]
nClass = len(np.unique(state_0.get_blocks().a))
print("%d classes, entropy %f, mean_field %f, bethe %f" % (nClass, entropy, L+sum(S_mf), L+S_bethe+sum(S_mf[1:])))

# Save final graph
fname = "NSBM_mcmc_%d_%f" % (nClass, entropy)
write_classes_hierarchical(os.path.join(outdir,fname+".tsv"), g, state)
pickle.dump([g, state, dls, pv, pe, S_mf, S_bethe], open(os.path.join(outdir,fname+".pickle"), "wb"), -1)
#g.save(os.path.join(outdir,fname+".gt.gz"))

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
