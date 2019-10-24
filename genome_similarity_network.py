#!/usr/bin/env python3

import os
import sys
import math
import argparse

parser = argparse.ArgumentParser(
    description='Group genomes on a network by genomic similarity')
parser.add_argument('sims', type=str,
                    help='genomic similarity input file')
parser.add_argument('column', type=str,
                    help='grouping column')
parser.add_argument('out_dir', type=str,
                    help='network output dir')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)
file_nodes = os.path.join(args.out_dir, os.path.splitext(os.path.basename(args.sims))[0]+'_nodes.tsv')
file_links = os.path.join(args.out_dir, os.path.splitext(os.path.basename(args.sims))[0]+'_links.tsv')

neighbourhood = {}  # For each genome, list with the genome itself and its neighbours
with open(args.sims) as fh_sim, open(file_links, 'w') as fh_lnk:
    header_data = next(fh_sim).strip().split('\t')
    idx = {}
    for i, h in enumerate(header_data):
        idx[h] = i

    fh_lnk.write('Source\tTarget\tType\tWeight\tANIp\tDist\tWI_i20D\tWI_i100D\tWI_5%\n')
    for line in fh_sim:
        items = line.strip().split('\t')
        query = items[idx['Query genome']]
        reference = items[idx['Reference genome']]
        similarity = items[idx[args.column]]

        if query not in neighbourhood:
            neighbourhood[query] = [query]
        if query == reference:
            continue

        ANIp = float(similarity)
        if (ANIp > 0):
            neighbourhood[query].append(reference)
            Dist = 1 - (ANIp / 100)
            WI_20 = 1 / (1 + 20*Dist)
            WI_100 = 1 / (1 + 100*Dist)
            tmp = (query, reference, 'Undirected',
                   '1', str(similarity), str(Dist),
                   str(WI_20), str(WI_100), '0.05')
            fh_lnk.write('\t'.join(tmp)+'\n')

grp_new = 1  # Next group to be assigned
genome_grp = {}  # Group already assigned for each genome
grp_members = {}  # Genomes already assigned to each group
for genome in neighbourhood:  # Cycle through each genome
    grp_nbh = set()  # List of groups already assigned on this neighbourhood
    for nb in neighbourhood[genome]:
        if nb in genome_grp:
            grp_nbh.add(genome_grp[nb])

    if len(grp_nbh) == 0:
        grp_ass = grp_new
        grp_new = grp_new + 1
        grp_members[grp_ass] = set()
    else:
        grp_ass = min(grp_nbh)
        if len(grp_nbh) > 1:
            for grp in grp_nbh:
                if grp != grp_ass:
                    for g in grp_members[grp]:
                        genome_grp[g] = grp_ass
                    grp_members[grp_ass].update(grp_members.pop(grp))
    for nb in neighbourhood[genome]:
        genome_grp[nb] = grp_ass
    grp_members[grp_ass].update(neighbourhood[genome])

with open(file_nodes, 'w') as fh_nod:
    fh_nod.write('ID\tGroup\n')
    for genome in sorted(neighbourhood.keys()):
        fh_nod.write(genome+'\tG'+str(genome_grp[genome])+'\n')
