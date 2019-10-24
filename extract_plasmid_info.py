#!/usr/bin/env python3

import os
import sys
import gzip
import argparse

parser = argparse.ArgumentParser(
    description='Extract plasmid info to table')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='plasmid list')
parser.add_argument('taxfile', type=str,
                    help='taxonomy lineage file')
parser.add_argument('datadir', type=str,
                    help='dirctory with plasmid sequence files')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout,
                    help='output file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

tax2lin={}
with gzip.open(args.taxfile, 'rt') as fh_tax:
    for line in fh_tax:
        if line.strip() == '':
            continue
        taxid, lineage = line.split('\t', 1)
        tax2lin[taxid] = lineage.strip()

header = [
    'Caption', 'SourceDB', 'AccessionVersion', 'MoleculeType', 'SeqName', 'Size',
    'Topology', 'UpdateDate', 'Title', 'TaxId', 'TaxName', 'TaxCategory',
    'TaxDivision', 'TaxLineage', 'TaxSuperkingdom', 'TaxPhylum', 'TaxClass', 'TaxOrder',
    'TaxFamily', 'TaxGenus', 'TaxSpecies', 'OrganismName', 'StrainName', 'IsolateName'
    ]

seq_info_fields = [
    'caption', 'source_db', 'refseq_sequence_acc', 'molecule_type',
    'sequence_name', 'size', 'topology', 'update_date', 'title', 'pubmed',
    'taxid', 'organism_name', 'strain_name', 'isolate_name'
    ]

args.outfile.write('\t'.join(header)+'\n')

for line in args.infile:
    accver = line.strip()
    if accver == '':
        continue

    with open(os.path.join(args.datadir, accver+'.fna')) as fh_fna:
        title = fh_fna.readline().strip().split(' ', 1)[1]

    with open(os.path.join(args.datadir, accver+'.gbff')) as fh_gbff:
        line = fh_gbff.readline()
        pubmed = []
        size = '-'
        topology = '-'
        organism_name = '-'
        strain_name = '-'
        isolate_name = '-'
        sequence_name = '-'
        taxid = '-'
        while True:
            if line == '':
                break
            if line == '\n':
                continue
            if line[0:6] == 'LOCUS ':
                size = line[29:40].strip()
                topology = line[55:63].strip()
                update_date = line[68:79].strip()
            if line.find('/organism="') != -1:
                organism_name = line.split('=')[1].strip().strip('"')
            elif line.find('/strain="') != -1:
                strain_name = line.split('=')[1].strip().strip('"')
            elif line.find('/isolate="') != -1:
                isolate_name = line.split('=')[1].strip().strip('"')
            elif line.find('/plasmid="') != -1:
                sequence_name = line.split('=')[1].strip().strip('"')
            elif line.find('/db_xref="taxon:') != -1:
                taxid = line.split(':')[1].strip().strip('"')
            if line[0:6] == 'CONTIG':
                break
            if line[0:6] == 'ORIGIN':
                break
            if line[0:2] == '//':
                break
            line = fh_gbff.readline()

    seq_info = []
    seq_info.append(accver.split('.')[0])
    seq_info.append('refseq')
    seq_info.append(accver)
    #seq_info.append(insd_accver)
    seq_info.append('Plasmid')
    seq_info.append(sequence_name)
    seq_info.append(size)
    seq_info.append(topology)
    seq_info.append(update_date)
    seq_info.append(title)
    seq_info.append(taxid)
    seq_info.append(tax2lin[taxid])
    seq_info.append(organism_name)
    seq_info.append(strain_name)
    seq_info.append(isolate_name)
    args.outfile.write('\t'.join(seq_info)+'\n')
