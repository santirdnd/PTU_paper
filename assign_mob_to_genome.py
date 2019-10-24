#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Assign MOB types to genomes')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='MOB genes list')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='assigned plasmids list')
parser.add_argument('-c', '--columns', type=str,
                    help='columns names')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

relaxases={}
for line in args.infile:
    if line.strip() == '':
        continue
    pl, mob = line.strip().split('\t', 1)
    if pl in relaxases:
        tmp = relaxases[pl].split(';')
        tmp.append(mob)
        relaxases[pl] = ';'.join(sorted(tmp))
    else:
        relaxases[pl] = mob

header = args.columns.strip().split(',')
args.outfile.write('\t'.join(header) + '\n')

for pl in relaxases:
    args.outfile.write(pl + '\t' + relaxases[pl] + '\n')
