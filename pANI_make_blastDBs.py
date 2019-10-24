#!/usr/bin/env python2

import os
import sys
import argparse
import subprocess as sp

parser = argparse.ArgumentParser(
    description='create BLASTdb for a list')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='source table file')
parser.add_argument('-o', '--outfolder', nargs='?', type=str, default='plasmiddb',
		    help='folder to save the databases')
parser.add_argument('-i', '--infolder', nargs='?', type=str, default='original',
		    help='folder to save the databases')
parser.add_argument('-dt', '--dtype', type=str, default='nucl',
		    choices=['nucl','prot'],
                    help='database type')
args = parser.parse_args()

def plasmiddb(filename,outfolder,dtype):
    out=outfolder+'/'+filename[:-4]
    filedir=os.path.join(args.infolder,filename)
    sp.call(['makeblastdb', '-in',filedir,'-out',out,'-dbtype', dtype])

for line in args.infile:
    fl= line.strip()+'.fna'
    plasmiddb(fl,args.outfolder,args.dtype)
