#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Calculate clusters density of a network')
parser.add_argument('nodes', type=argparse.FileType('r'),
                    help='network nodes file')
parser.add_argument('links', type=argparse.FileType('r'),
                    help='network links file')
parser.add_argument('output', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='cluster densities output file')
parser.add_argument('-i,', '--id_col', type=str,
                    default='accessionversion',
                    help='node identifier column')
parser.add_argument('-c,', '--cluster_col', type=str,
                    default='pgroup',
                    help='cluster definition column')
parser.add_argument('-s,', '--source_col', type=str,
                    default='Source',
                    help='link source column')
parser.add_argument('-t,', '--target_col', type=str,
                    default='Target',
                    help='link target column')
parser.add_argument('-w', '--weight_col', type=str,
                    default='anip',
                    help='weights definition column')
parser.add_argument('-f', '--filter_nodes', type=argparse.FileType('r'),
                    help='file with list of nodes to filter from network')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()


filter = False
filter_lst = []
if args.filter_nodes is not None:
    filter = True
    for line in args.filter_nodes:
        filter_lst.append(line.strip())

nodes_hdr = next(args.nodes).strip().split('\t')
nodes_idx = {}
for i, h in enumerate(nodes_hdr):
    nodes_idx[h] = i

links_hdr = next(args.links).strip().split('\t')
links_idx = {}
for i, h in enumerate(links_hdr):
    links_idx[h] = i

nodes = {}
clusters = {}
for line in args.nodes:
    items = line.strip().split('\t')
    node = items[nodes_idx[args.id_col]]
    cluster = items[nodes_idx[args.cluster_col]]
    if filter and (node in filter_lst):
        continue
    if node in nodes:
        print('Error: Duplicated node ' + node, file=sys.stderr)
        exit()
    nodes[node] = cluster
    if cluster not in clusters:
        clusters[cluster] = []
    clusters[cluster].append(node)

links = {}
loop_weight = 100
looped_graph = False
unmerged_links = False
for line in args.links:
    items = line.strip().split('\t')
    source = items[links_idx[args.source_col]]
    target = items[links_idx[args.target_col]]
    weight = items[links_idx[args.weight_col]]
    if filter and ((source in filter_lst) or (target in filter_lst)):
        continue
    if source not in links:
        links[source] = {}
    if target not in links[source]:
        links[source][target] = weight
    else:
        print('Error: Duplicated link ' + source + ' -> ' + target, file=sys.stderr)
        exit()
    if source == target:
        if not looped_graph:
            looped_graph = True
            print('Warning: Network with loops', file=sys.stderr)
        if float(weight) != loop_weight:
            print('Warning: Weight (' + weight + ') of loop of node ' + source + ' differs from its expected value (' + str(loop_weight_value) + ')', file=sys.stderr)
    else:
        if (not unmerged_links) and \
                (target in links) and (source in links[target]):
            unmerged_links = True
            print('Warning: Network with unmerged links', file=sys.stderr)

l = 0
matrix = {}
for i in nodes:
    matrix[i] = {}
    for j in nodes:
        matrix[i][j] = 0
for i in nodes:
    if i in links:
        for j in nodes:
            if j in links[i]:
                if j == i:
                    matrix[i][j] = links[i][j]
                else:
                    l = l + 1
                    matrix[i][j] = links[i][j]
                    matrix[j][i] = links[i][j]

n = len(nodes)
d = l / (n * (n - 1) / 2)
# print('Number of nodes |G|: n = ' + str(n))
# print('Number of edges = ' + str(l))
# print('Average link density: δ(G) = ' + str(d))
# print()
# print('Undefined label: -')
# print('    Number of undefined nodes:' + str(len(clusters['-'])))
# print()

args.output.write('\t'.join(('Cluster', '|C| = n_C', 'l_C', \
        'l_int_C', 'l_int_C_Theo', 'δ_int_C(G)', \
        'l_ext_C', 'l_ext_C_Theo', 'δ_ext_C(G)')) + '\n')
for cluster in sorted(clusters):
    if cluster == '-':
        continue
    n_C = len(clusters[cluster])
    l_C = 0
    l_int_C = 0
    l_ext_C = 0
    for i in clusters[cluster]:
        for j in matrix[i]:
            if matrix[i][j] == 0:
                continue
            if nodes[j] == cluster:
                if i < j:
                    l_C = l_C + 1
                    l_int_C = l_int_C + 1
            else:
                l_C = l_C + 1
                l_ext_C = l_ext_C + 1
    l_int_C_Theo = int(n_C * (n_C - 1) / 2)
    l_ext_C_Theo = n_C * (n - n_C)
    d_int_C = l_int_C / l_int_C_Theo
    d_ext_C = l_ext_C / l_ext_C_Theo
    # print('Cluster: ' + cluster)
    # print('    Number of nodes of C |C|: n_C = ' + str(n_C))
    # print('    Number of edges of C = ' + str(l_C))
    # print('    Internal edges of C = ' + str(l_int_C) + ' (' + str(l_int_C_Theo) + ')')
    # print('    Inter-cluster edges of C = ' + str(l_ext_C) + ' (' + str(l_ext_C_Theo) + ')')
    # print('    Intra-cluster density of C: δ_int_C(G) = ' + str(d_int_C))
    # print('    Inter-cluster density of C: δ_ext_C(G) = ' + str(d_ext_C))
    # print()
    args.output.write('\t'.join((cluster, str(n_C), str(l_C), \
        str(l_int_C), str(l_int_C_Theo), str(d_int_C), \
        str(l_ext_C), str(l_ext_C_Theo), str(d_ext_C))) + '\n')

args.output.write('#Number of nodes\t' + str(n) + '\n')
args.output.write('#Number of edges\t' + str(l) + '\n')
args.output.write('#Average link density δ(G)\t' + str(d) + '\n')
args.output.write('#Number of undefined nodes\t' + str(len(clusters['-'])) + '\n')
