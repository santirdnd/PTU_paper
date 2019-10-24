#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

THRESHOLDS=(80.00 85.00 90.00 95.00)

BASEDIR=plasmidfinder
mkdir -p ${BASEDIR}

DBDIR=databases
cp ${DBDIR}/config_plasmidfinder ${DBDIR}/config

for threshold in "${THRESHOLDS[@]}"; do
    thr="${threshold//.}"
    thr="${thr:0:2}"
    f_res=${BASEDIR}/results_ent_gpos_${thr}.tsv
    f_pfinder=${BASEDIR}/pfinder${thr}.tsv

    OUTDIR=${BASEDIR}/pf_ent_${thr}
    plasmidfinder.pl -d ${DBDIR}/ -i plasmid.genomic.fna -o ${OUTDIR} -p enterobacteriaceae -k ${threshold}
    echo ''
    f_hits=${OUTDIR}/results_tab.txt
    cat ${f_hits} > ${f_res}

    OUTDIR=${BASEDIR}/pf_pos_${thr}
    plasmidfinder.pl -d ${DBDIR}/ -i plasmid.genomic.fna -o ${OUTDIR} -p gram_positive -k ${threshold}
    echo ''
    f_hits=${OUTDIR}/results_tab.txt
    sed '1,2d' ${f_hits} >> ${f_res}

    sed '1,2d' ${f_res} | cut -f1,4 | ./assign_pfinder_to_genome.py - ${f_pfinder} -c Acc_Num,PFinder_${thr},PFinder_${thr}smpl
done

./append_columns_to_file.py plasmid_mob.tsv ${BASEDIR}/pfinder80.tsv plasmid_tmp.tsv -ik AccessionVersion -ek Acc_Num -l PFinder_80,PFinder_80smpl -d '-'
./append_columns_to_file.py plasmid_tmp.tsv ${BASEDIR}/pfinder95.tsv plasmid_mob_pfinder.tsv -ik AccessionVersion -ek Acc_Num -l PFinder_95,PFinder_95smpl -d '-'
rm plasmid_tmp.tsv

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.
