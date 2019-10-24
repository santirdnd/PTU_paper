#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Assign PlasmidFinder Replicon types to genomes')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='Replicon genes list')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='assigned plasmids list')
parser.add_argument('-c', '--columns', type=str,
                    help='columns names')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

replicons={}
reps_smpl={}
for line in args.infile:
    if line.strip() == '':
        continue
    rep, pl = line.strip().split('\t', 1)
    rep_smpl = rep.strip().split('(', 1)[0]
    if pl in replicons:
        tmp = replicons[pl].split(';')
        tmp.append(rep)
        replicons[pl] = ';'.join(sorted(tmp))

        tmp = reps_smpl[pl].split(';')
        tmp.append(rep_smpl)
        reps_smpl[pl] = ';'.join(sorted(tmp))
    else:
        replicons[pl] = rep
        reps_smpl[pl] = rep_smpl

header = args.columns.strip().split(',')
args.outfile.write('\t'.join(header) + '\n')

for pl in replicons:
    args.outfile.write(pl + '\t' + replicons[pl] + '\t' + reps_smpl[pl] + '\n')
