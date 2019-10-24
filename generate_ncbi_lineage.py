#!/usr/bin/env python3

import os
import sys
import gzip
import tarfile
import argparse

parser = argparse.ArgumentParser(
    description='Generate NCBI TaxId to Lineage table')
parser.add_argument('infile', type=str,
                    help='NCBI taxonomy dump file')
parser.add_argument('-c', '--catfile', type=str,
                    help='NCBI taxonomy categories file')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='output file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

with tarfile.open(args.infile, 'r') as fh_tar:
    fh_tar.extract('names.dmp')
    fh_tar.extract('nodes.dmp')
    fh_tar.extract('merged.dmp')
    fh_tar.extract('delnodes.dmp')
    fh_tar.extract('division.dmp')

names = {}
with open('names.dmp') as fh:
    for line in fh:
        if 'scientific name' in line:
            items = line.split('|')
            names[int(items[0])] = items[1].strip()
os.remove('names.dmp')

nodes = {}
with open('nodes.dmp') as fh:
    for line in fh:
        items = line.split('|')
        nodes[int(items[0])] = (int(items[1]), items[2].strip(), int(items[4]))
os.remove('nodes.dmp')

merged = {}
with open('merged.dmp') as fh:
    for line in fh:
        items = line.split('|')
        merged[int(items[0])] = int(items[1])
os.remove('merged.dmp')

delnodes = []
with open('delnodes.dmp') as fh:
    for line in fh:
        delnodes.append(int(line.split()[0]))
os.remove('delnodes.dmp')

division = {}
with open('division.dmp') as fh:
    for line in fh:
        items = line.split('|')
        division[int(items[0])] = items[2].strip()
os.remove('division.dmp')

if args.catfile:
    with tarfile.open(args.catfile, 'r') as fh_tar:
        fh_tar.extract('categories.dmp')

    categories = {}
    with open('categories.dmp') as fh:
        for line in fh:
            items = line.split()
            categories[int(items[2])] = items[0]
    os.remove('categories.dmp')

for tax_id in sorted(nodes):
    tax_vals = nodes[tax_id]
    tax_name = names[tax_id]
    lin_full = []
    lin_full.insert(0, tax_name)
    lin_rank = {
        'superkingdom': '-',
        'phylum': '-',
        'class': '-',
        'order': '-',
        'family': '-',
        'genus': '-',
        'species': '-'
        }
    if tax_vals[1] in lin_rank:
        lin_rank[tax_vals[1]] = tax_name

    tmp_id = tax_id
    tmp_vals = tax_vals
    while tmp_id != 1:
        tmp_id = tmp_vals[0]
        tmp_vals = nodes[tmp_id]
        tmp_name = names[tmp_id]
        lin_full.insert(0, tmp_name)
        if tmp_vals[1] in lin_rank:
            lin_rank[tmp_vals[1]] = tmp_name

    out_vals = []
    out_vals.append(str(tax_id))
    out_vals.append(tax_name)
    if args.catfile:
        out_vals.append(categories.get(tax_id, '-'))
    else:
        out_vals.append('-')
    out_vals.append(division[tax_vals[2]])
    out_vals.append(';'.join(lin_full))
    out_vals.append(lin_rank['superkingdom'])
    out_vals.append(lin_rank['phylum'])
    out_vals.append(lin_rank['class'])
    out_vals.append(lin_rank['order'])
    out_vals.append(lin_rank['family'])
    out_vals.append(lin_rank['genus'])
    out_vals.append(lin_rank['species'])
    args.outfile.write('\t'.join(out_vals) + '\n')

for tax_id in sorted(merged):
    tax_id_new = merged[tax_id]
    tax_vals = nodes[tax_id_new]
    tax_name = names[tax_id_new]
    lin_full = []
    lin_full.insert(0, tax_name)
    lin_rank = {
        'superkingdom': '-',
        'phylum': '-',
        'class': '-',
        'order': '-',
        'family': '-',
        'genus': '-',
        'species': '-'
        }
    if tax_vals[1] in lin_rank:
        lin_rank[tax_vals[1]] = tax_name

    tmp_id = tax_id_new
    tmp_vals = tax_vals
    while tmp_id != 1:
        tmp_id = tmp_vals[0]
        tmp_vals = nodes[tmp_id]
        tmp_name = names[tmp_id]
        lin_full.insert(0, tmp_name)
        if tmp_vals[1] in lin_rank:
            lin_rank[tmp_vals[1]] = tmp_name

    out_vals = []
    out_vals.append(str(tax_id))
    out_vals.append(tax_name)
    if args.catfile:
        out_vals.append(categories.get(tax_id_new, '-'))
    else:
        out_vals.append('-')
    out_vals.append(division[tax_vals[2]])
    out_vals.append(';'.join(lin_full))
    out_vals.append(lin_rank['superkingdom'])
    out_vals.append(lin_rank['phylum'])
    out_vals.append(lin_rank['class'])
    out_vals.append(lin_rank['order'])
    out_vals.append(lin_rank['family'])
    out_vals.append(lin_rank['genus'])
    out_vals.append(lin_rank['species'])
    args.outfile.write('\t'.join(out_vals) + '\n')

for tax_id in sorted(delnodes):
    out_vals = []
    out_vals.append(str(tax_id))
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('DELETED_-')
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('-')
    out_vals.append('-')
    args.outfile.write('\t'.join(out_vals) + '\n')

