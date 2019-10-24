#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

while IFS='' read -r f || [[ -n "$f" ]]; do
    acc="${f%.*}"
    mv data/$acc.gbff data/$f.gbff

    f_orig_gbff=data/$f.gbff
    f_orig_fna=data/$f.fna
    f_orig_gbk=data/$f.gbk
    f_orig_base=data/$f

    ./fix_ncbi_gb.py $f_orig_gbff $f_orig_fna $f_orig_gbk
    ./generate_auxiliary_genome_files.py -tt 11 -c -g $f_orig_gbk $f_orig_base

    if [ -s $f_orig_base.faa ]; then
        mv $f_orig_base.faa $f_orig_base.tmp
        cat $f_orig_base.tmp | awk '/^>/ { print (NR==1 ? "" : RS) $0; next } { printf "%s", $0 } END { printf RS }' > $f_orig_base.faa
        mv $f_orig_base.fcn $f_orig_base.tmp
        cat $f_orig_base.tmp | awk '/^>/ { print (NR==1 ? "" : RS) $0; next } { printf "%s", $0 } END { printf RS }' > $f_orig_base.fcn
        rm $f_orig_base.tmp
    else
        echo $f >> plasmid_no_cds.lst
    fi
done < "$1"

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.

