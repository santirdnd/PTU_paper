#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

INPUT=plasmid_mob_pfinder.tsv
BADLIST=plasmid_bad.lst
OUTPUT1=plasmid_mob_pfinder_filt.tsv

awk -F"\t" 'NR==FNR{a[$1];next} {if ($3 in a) {print $0 "\tYes"} else if (FNR==1) {print $0 "\tFiltered"} else {print $0 "\tNo"}}' ${BADLIST} ${INPUT} > ${OUTPUT1}

PGROUPS=pGroups_181128.tsv
OUTPUT2=plasmid_mob_pfinder_filt_pTU.tsv.tmp

./append_columns_to_file.py ${OUTPUT1} ${PGROUPS} ${OUTPUT2} -ik AccessionVersion -ek ID -l pTU_Manual -d '-'

PGROUPS=auto_pTUs/plasmid_assignment_kept_190823.tsv
OUTPUT3=plasmid_mob_pfinder_filt_pTU.tsv

./append_columns_to_file.py ${OUTPUT2} ${PGROUPS} ${OUTPUT3} -ik AccessionVersion -ek AccessionVersion -l pTU_PID,HRange,Mobilizable -d '-'
rm ${OUTPUT2}

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.
