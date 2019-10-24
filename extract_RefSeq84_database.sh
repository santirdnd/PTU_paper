#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

REFSEQ84_FILES=/fernando/databases/RefSeq84/plasmid

gunzip -c ${REFSEQ84_FILES}/plasmid.1.1.genomic.fna.gz | awk '/^>/ { print (NR==1 ? "" : RS) $0; next } { printf "%s", $0 } END { printf RS }' > plasmid.genomic.fna
gunzip -c ${REFSEQ84_FILES}/plasmid.2.1.genomic.fna.gz | awk '/^>/ { print (NR==1 ? "" : RS) $0; next } { printf "%s", $0 } END { printf RS }' >> plasmid.genomic.fna
gunzip -c ${REFSEQ84_FILES}/plasmid.3.1.genomic.fna.gz | awk '/^>/ { print (NR==1 ? "" : RS) $0; next } { printf "%s", $0 } END { printf RS }' >> plasmid.genomic.fna

gunzip -c ${REFSEQ84_FILES}/plasmid.1.genomic.gbff.gz > plasmid.genomic.gbff
gunzip -c ${REFSEQ84_FILES}/plasmid.2.genomic.gbff.gz >> plasmid.genomic.gbff
gunzip -c ${REFSEQ84_FILES}/plasmid.3.genomic.gbff.gz >> plasmid.genomic.gbff

./split_seqs.py -f fasta -e fna plasmid.genomic.fna data
./split_seqs.py -f gb -e gbff plasmid.genomic.gbff data

grep '^>' plasmid.genomic.fna | cut -d' ' -f1 | cut -d'>' -f2 > plasmid.lst

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.

