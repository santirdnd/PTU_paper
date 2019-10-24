#!/usr/bin/env python3

import os
import sys
import shlex
import argparse
import subprocess as sp

parser = argparse.ArgumentParser(
    description='Generate AccNET Representatives.fcn')
parser.add_argument('indir', type=str,
                    help='AccNET directory')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

pc = sp.run('ls ' + os.path.join(shlex.quote(args.indir),'*.faa') + ' | ' + \
            'grep -v "Representatives.faa" | cut -d"/" -f3 | sed "s/\.faa$//"',
            stdout=sp.PIPE, stderr=sp.PIPE,
            universal_newlines=True, check=True, shell=True)
acc_lst = {}
for idx, acc in enumerate(pc.stdout.splitlines(), 1):
    acc_lst[str(idx)] = acc

ren_lst = {}
with open(os.path.join(args.indir, 'rename.tmp')) as fh_ren:
    for line in fh_ren:
        if line.strip() == '':
            continue
        cl, id = line.strip().split('\t')
        ren_lst[id] = cl

with open(os.path.join(args.indir, 'kclust', 'representatives.fas')) as fh_rep, \
        open(os.path.join(args.indir, 'Representatives.fcn'), 'w') as fh_out:
    for line in fh_rep:
        if line.strip() == '':
            continue
        if line[0] == '>':
            rep = line.strip()
            idx = rep.split('|')[0][1:]
            prt = rep.split('|')[1]
            clu = '>'+ren_lst[rep]
            f_seq = os.path.join('original', acc_lst[idx]+'.fcn')
            with open(f_seq) as fh_seq:
                num = 0
                for l in fh_seq:
                    if l.strip() == '':
                        continue
                    if l[0] == '>':
                       num = num + 1
                       if num == int(prt):
                           fh_out.write(clu+'\n')
                       continue
                    if num == int(prt):
                        fh_out.write(l)
