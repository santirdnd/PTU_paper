#!/usr/bin/env python3

import os
import sys
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.Data import CodonTable
from BCBio import GFF

parser = argparse.ArgumentParser(
    description='Generate auxiliary files (fna, faa and gff) from GenBank file')
parser.add_argument('gbk', type=str,
                    help='source gbk file')
parser.add_argument('basename', nargs='?', type=str,
                    default=None,
                    help='basename of output files')
parser.add_argument('-c', '--contigs',
                    action='store_false', default=True,
                    help='do not output nucleotide fasta file of contigs')
parser.add_argument('-a', '--aminoacids',
                    action='store_false', default=True,
                    help='do not output aminoacid fasta file of CDSs')
parser.add_argument('-n', '--nucleotides',
                    action='store_false', default=True,
                    help='do not output nucleotide fasta file of CDSs')
parser.add_argument('-g', '--gff',
                    action='store_false', default=True,
                    help='do not output GFF format file')
parser.add_argument('-l', '--locus_tag',
                    action='store_true', default=False,
                    help='insert locus_tag in description of hypothetical proteins')
parser.add_argument('-s', '--strict',
                    action='store_true', default=False,
                    help='strict protein translation check')
parser.add_argument('-tt', '--translation_table', type=int,
                    help='NCBI Translation Table number or Genetic Code id for protein translation')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if not args.basename:
    basename = os.path.splitext(os.path.basename(args.gbk))[0]
    # TODO: Comprobar que no existan ficheros con este basename y sólo continuar si se usó la opción --force
else:
    basename = args.basename

if args.translation_table:
    if args.translation_table not in CodonTable.ambiguous_dna_by_id:
        print(os.path.basename(sys.argv[0]) + ':',
              'error: unknown translation table id', args.translation_table, file=sys.stderr)
        sys.exit(1)
    else:
        translation_table = CodonTable.ambiguous_dna_by_id[args.translation_table]

if args.gff:
    with open(args.gbk, 'r') as fh_gbk, open(basename + '.gff', 'w') as fh_gff:
        GFF.write(SeqIO.parse(fh_gbk, 'genbank'), fh_gff)

with open(args.gbk, 'r') as fh_gbk:
    if args.contigs:
        fh_fna = open(basename + '.fna', 'w')
    if args.aminoacids:
        fh_faa = open(basename + '.faa', 'w')
    if args.nucleotides:
        fh_fcn = open(basename + '.fcn', 'w')

    for seq_record_gbk in SeqIO.parse(fh_gbk, 'genbank'):
        if args.contigs:
            seq_record_fna = SeqRecord(seq_record_gbk.seq)
            # seq_record_fna.seq.alphabet = IUPAC.extended_dna
            seq_record_fna.id = seq_record_gbk.id
            seq_record_fna.description = seq_record_gbk.description
            SeqIO.write(seq_record_fna, fh_fna, 'fasta')

        if args.aminoacids or args.nucleotides:
            for feature in seq_record_gbk.features:
                if feature.type == 'CDS':
                    if('pseudo' in feature.qualifiers) or ('pseudogene' in feature.qualifiers)\
                            or ('translation' not in feature.qualifiers):
                        continue
                    seq_record_faa = SeqRecord(Seq(feature.qualifiers['translation'][0], IUPAC.extended_protein))
                    if args.aminoacids:
                        seq_record_faa.id = feature.qualifiers['protein_id'][0]
                        if 'product' in feature.qualifiers:
                            seq_record_faa.description = feature.qualifiers['product'][0]
                        else:
                            seq_record_faa.description = 'unnamed protein product'
                        if args.locus_tag:
                            if feature.qualifiers['product'][0] == 'hypothetical protein':
                                seq_record_faa.description += ' ' + feature.qualifiers['locus_tag'][0]
                        # TODO
                        # if 'plasmid' in seq_record_gbk.description:
                        #     seq_record_faa.description += ' (plasmid)'
                        # if args.phage:
                        #     seq_record_faa.description += ' (phage)'
                        # seq_record_faa.description += ' [' + seq_record_gbk.description + ']'
                        SeqIO.write(seq_record_faa, fh_faa, 'fasta')
                    if args.nucleotides:
                        # seq_record_fcn = feature.extract(seq_record_gbk)
                        seq_record_fcn = SeqRecord(Seq(str(feature.extract(seq_record_gbk).seq), IUPAC.extended_dna))
                        try:
                            if args.translation_table:
                                seq_cds = seq_record_fcn.seq.translate(table=translation_table, cds=True)
                            else:
                                seq_cds = seq_record_fcn.seq.translate(table=feature.qualifiers['transl_table'][0], cds=True)
                        except CodonTable.TranslationError as err:
                            print(os.path.basename(sys.argv[0]) + ':',
                                  'error:', err, file=sys.stderr)
                            print(os.path.basename(sys.argv[0]) + ':',
                                  'error: non-matching translation of', feature.qualifiers['protein_id'][0],
                                  file=sys.stderr)
                            if args.strict:
                                sys.exit(1)
                        else:
                            if seq_cds != seq_record_faa.seq:
                                print(os.path.basename(sys.argv[0]) + ':',
                                      'error: non-matching translation of', feature.qualifiers['protein_id'][0],
                                      file=sys.stderr)
                                if args.strict:
                                    sys.exit(1)
                        seq_record_fcn.id = feature.qualifiers['protein_id'][0]
                        if 'product' in feature.qualifiers:
                            seq_record_fcn.description = feature.qualifiers['product'][0]
                        else:
                            seq_record_fcn.description = 'unnamed protein product'
                        if args.locus_tag:
                            if feature.qualifiers['product'][0] == 'hypothetical protein':
                                seq_record_fcn.description += ' ' + feature.qualifiers['locus_tag'][0]
                        # TODO
                        # if 'plasmid' in seq_record_gbk.description:
                        #     seq_record_fcn.description += ' (plasmid)'
                        # if args.phage:
                        #     seq_record_fcn.description += ' (phage)'
                        # seq_record_fcn.description += ' [' + seq_record_gbk.description + ']'
                        SeqIO.write(seq_record_fcn, fh_fcn, 'fasta')

    if args.contigs:
        fh_fna.close()
    if args.aminoacids:
        fh_faa.close()
    if args.nucleotides:
        fh_fcn.close()
