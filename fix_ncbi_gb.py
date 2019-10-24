#!/usr/bin/env python3

import os
import sys
import argparse
from Bio import SeqIO
from Bio.Alphabet import IUPAC

parser = argparse.ArgumentParser(
    description='Fix NCBI GenBank file inserting genome nucleotide sequence to ORIGIN section and protein translations')
parser.add_argument('gbk', type=argparse.FileType('r'),
                    help='source gbk file')
parser.add_argument('fna', type=argparse.FileType('r'),
                    help='source genome nucleotide fasta file')
parser.add_argument('fixed_gbk', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='processed gbk file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()


for seq_gbk, seq_fna in zip(SeqIO.parse(args.gbk, 'genbank'), SeqIO.parse(args.fna, 'fasta')):
    seq_gbk.seq = seq_fna.seq
    seq_gbk.seq.alphabet = IUPAC.ambiguous_dna
    SeqIO.write(seq_gbk, args.fixed_gbk, 'genbank')

# Warning: GenBank metadata is not saved exactly as the original
