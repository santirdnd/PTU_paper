#!/bin/bash

start_time=`date +%s`
echo 'Starting ...'
date

DATADIR=original
PLASMIDS=plasmid.lst

WINDOW=250
STEP=50
SPLITDIR=${DATADIR}/splits
BLASTDB=${DATADIR}/plasmiddb

mkdir -p ${SPLITDIR}
mkdir -p ${BLASTDB}

./pANI_split_fasta.py ${PLASMIDS} -seq ${DATADIR} -w ${WINDOW} -s ${STEP} -sf ${SPLITDIR}
./pANI_make_blastDBs.py ${PLASMIDS} -o ${BLASTDB} -i ${DATADIR} -dt nucl

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr ${end_time} - ${start_time}` s.
