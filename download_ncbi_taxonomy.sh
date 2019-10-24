#!/usr/bin/env bash

SERVER_PATH='ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy'
DATE=`date +%y%m%d`

echo 'Starting ...'
date

mkdir -p taxonomy_$DATE
cd taxonomy_$DATE

wget -nv --show-progress $SERVER_PATH/taxdump_readme.txt
wget -nv --show-progress $SERVER_PATH/taxdump.tar.gz
wget -nv --show-progress $SERVER_PATH/taxcat_readme.txt
wget -nv --show-progress $SERVER_PATH/taxcat.tar.gz

./generate_ncbi_lineage.py -c taxcat.tar.gz taxdump.tar.gz | gzip > taxlineage.tsv.gz

date
echo 'Job successfully processed.'
