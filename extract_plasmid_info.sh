#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

PLASMIDS=plasmid.lst
TAXINFO=taxonomy_171124/taxlineage.tsv.gz
DATADIR=data
PLSMTABL=plasmid.tsv

./extract_plasmid_info.py ${PLASMIDS} ${TAXINFO} ${DATADIR} ${PLSMTABL}

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.
