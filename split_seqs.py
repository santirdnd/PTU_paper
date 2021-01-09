#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Split sequences from file to directory')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='input sequences file')
parser.add_argument('subdir', type=str,
                    help='directory to output sequences')
parser.add_argument('-e', '--ext', type=str,
                    help='extension of output files')
parser.add_argument('-f', '--format', type=str,
                    default='fasta',
                    choices=['fasta', 'fastq', 'fastq-sanger', 'fastq-solexa', 'fastq-illumina', 'genbank', 'gb'],
                    help='file format')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if args.format == 'genbank' or args.format == 'gb':
    if args.ext:
        ext = args.ext
    else:
        ext = 'gb'
    fmark = 'LOCUS'
elif args.format == 'fasta':
    if args.ext:
        ext = args.ext
    else:
        ext = 'fasta'
    fmark = '>'
else:
    if args.ext:
        ext = args.ext
    else:
        ext = 'fastq'
    fmark = '@'

os.makedirs(args.subdir, exist_ok=True)

fh = None
for line in args.file:
    if line.startswith(fmark):
        if args.format == 'genbank' or args.format == 'gb':
            record_id = line.split()[1]
        else:
            record_id = line.split()[0][1:]
        filename = '.'.join((record_id, ext))
        if fh:
            fh.close()
        fh = open(os.path.join(args.subdir, filename), 'w')
        fh.write(line)
    else:
        if fh:
            fh.write(line)
