#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

OUTDIR=mobscan
mkdir -p $OUTDIR

MOBfamDB='databases/MOBfamDB'

f_faa=$OUTDIR/allprot.faa
f_res=$OUTDIR/results
f_res60=$OUTDIR/results_60.tsv
f_res70=$OUTDIR/results_70.tsv
f_mob60=$OUTDIR/mob60.tsv
f_mob70=$OUTDIR/mob70.tsv

# while IFS='' read -r f || [[ -n "$f" ]]; do
#     sed "s/^>/>$f|/" data/$f.faa >> $f_faa
# done < "$1"

# hmmscan --cpu 9 --incE 0.01 --incdomE 0.01 -o $f_res.log --domtblout $f_res.dom.log $MOBfamDB $f_faa
# ./hmmscan_domtblout_summarize.py -e 0.01 -i 0.01 -c 0.6 $f_res.dom.log $f_res60
# ./hmmscan_domtblout_summarize.py -e 0.01 -i 0.01 -c 0.7 $f_res.dom.log $f_res70

sed 's/|/\t/' $f_res60 | cut -f1,3 | ./assign_mob_to_genome.py - $f_mob60 -c Acc_Num,MOB_60
./append_columns_to_file.py plasmid.tsv $f_mob60 plasmid_tmp.tsv -ik AccessionVersion -ek Acc_Num -l MOB_60 -d '-'

sed 's/|/\t/' $f_res70 | cut -f1,3 | ./assign_mob_to_genome.py - $f_mob70 -c Acc_Num,MOB_70
./append_columns_to_file.py plasmid_tmp.tsv $f_mob70 plasmid_mob.tsv -ik AccessionVersion -ek Acc_Num -l MOB_70 -d '-'

rm plasmid_tmp.tsv

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.
