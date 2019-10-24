#!/usr/bin/env python2

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='calculate pANI values')
parser.add_argument('querylist', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='source table file')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='results output')
parser.add_argument('-rf', '--rstfolder', nargs='?', type=str, default='results',
                    help='BLAST pairwaise comparations folder')
parser.add_argument('-i', '--identity', nargs='?', type=int, default=225,
                        help='number of identical nucleotides per window')

args = parser.parse_args()


plaslist = []
for line in args.querylist:
    plaslist.append(line.strip())

number_hits = {}
sum_identity_filt = {}
sum_identity_total = {}
for query in plaslist:
    filedir = os.path.join(args.rstfolder,query+'.b6')
    infile = open(filedir,'r')

    number_hits[query] = {}
    sum_identity_filt[query] = {}
    sum_identity_total[query] = {}

    for line in infile:
        items = line.strip().split('\t')
        ref = items[1]
        pident = float(items[3])

        if int(items[2])>=args.identity:
            number_hits[query][ref] = number_hits[query].get(ref, 0) + 1
            sum_identity_filt[query][ref] = sum_identity_filt[query].get(ref, 0) + pident
        sum_identity_total[query][ref] = sum_identity_total[query].get(ref, 0) + pident

    infile.close()

args.outfile.write('Query\tReference\tHits\tWindows\tRW\tRI1\tRI2\tRI3\n')
for k in plaslist:
    posiblehits=number_hits[k][k]
    for v in plaslist:
        realhits=number_hits[k].get(v, 0)
        ident_filt=sum_identity_filt[k].get(v, 0)
        ident_total=sum_identity_total[k].get(v, 0)

        if realhits == 0:
            items = [k, v, '0', str(posiblehits), '0', '0', '0', str(ident_total/posiblehits)]
        else:
            items = [k, v, str(realhits), str(posiblehits), \
                     str((float(realhits)/posiblehits)*100), \
                     str(ident_filt/realhits), str(ident_filt/posiblehits), \
                     str(ident_total/posiblehits)]

        args.outfile.write('\t'.join(items)+'\n')
