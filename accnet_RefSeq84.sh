#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

OUTDIR=accnet/wgRefSeq84_fixed
ORIGDIR=../..
DATADIR=data
COLORDIR=color_rules
METADATA=plasmid_mob_pfinder_pGroup_filt.tsv

mkdir -p ${OUTDIR}

#while IFS='' read -r f || [[ -n "${f}" ]]; do
#    cp ${DATADIR}/${f}.faa ${OUTDIR}
#done < "$1"

#cd ${OUTDIR}
#accnet.pl --clean=no --fast=yes --threshold 1.1 --in *.faa --kp '-s 1.12 -c 0.8 -e 1e-4 -M 35000MB'

#cd ${ORIGDIR}
./append_columns_to_file.py ${OUTDIR}/Table.csv ${METADATA} ${OUTDIR}/Table2.tsv -ik ID -ek Caption -d ''
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/plasmid_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color -d '#000000'
./append_columns_to_file.py ${OUTDIR}/Table2.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table3.tsv -ik ID -ek Caption -l Color -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/mob60_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_MOB60 -d '#000000'
./append_columns_to_file.py ${OUTDIR}/Table3.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table4.tsv -ik ID -ek Caption -l Color_MOB60 -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/mob70_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_MOB70 -d '#000000'
./append_columns_to_file.py ${OUTDIR}/Table4.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table5.tsv -ik ID -ek Caption -l Color_MOB70 -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/skingdom_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_Superkingdom -d '#000000'
./append_columns_to_file.py ${OUTDIR}/Table5.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table6.tsv -ik ID -ek Caption -l Color_Superkingdom -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/phylum_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_Phylum -d '#999999'
./append_columns_to_file.py ${OUTDIR}/Table6.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table7.tsv -ik ID -ek Caption -l Color_Phylum -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/proteobact_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_Proteobacteria -d '#000000'
./append_columns_to_file.py ${OUTDIR}/Table7.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table8.tsv -ik ID -ek Caption -l Color_Proteobacteria -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/gammaprot_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_GammaProteobacteria -d '#000000'
./append_columns_to_file.py ${OUTDIR}/Table8.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table9.tsv -ik ID -ek Caption -l Color_GammaProteobacteria -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/enterobact_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_Enterobacteriaceae -d '#999999'
./append_columns_to_file.py ${OUTDIR}/Table9.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table10.tsv -ik ID -ek Caption -l Color_Enterobacteriaceae -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/pfamily_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_pFamily -d '#DDDDCC'
./append_columns_to_file.py ${OUTDIR}/Table10.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table11.tsv -ik ID -ek Caption -l Color_pFamily -d '#D9D9D9'
./assign_values_from_rules.py ${METADATA} ${COLORDIR}/pgroup_color_rules.tsv ${COLORDIR}/tmp_colors.tsv -k Caption -l Color_pGroup -d '#DDDDCC'
./append_columns_to_file.py ${OUTDIR}/Table11.tsv ${COLORDIR}/tmp_colors.tsv ${OUTDIR}/Table12.tsv -ik ID -ek Caption -l Color_pGroup -d '#D9D9D9'

date
echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr ${end_time} - ${start_time}` s.
