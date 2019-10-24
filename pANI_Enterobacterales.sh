#!/bin/bash

start_time=`date +%s`
echo 'Starting ...'
date

DATADIR=original
PLASMIDS=plasmid_Enterobacterales.lst

SPLITDIR=${DATADIR}/splits
BLASTDB=${DATADIR}/plasmiddb

OUTDIR=pANI_Enterobacterales
OUTBLAST=${OUTDIR}/blast_results

THREADS=50

mkdir -p ${OUTDIR}
mkdir -p ${OUTBLAST}

#./pANI_BLAST.py ${PLASMIDS} ${SPLITDIR} -df ${BLASTDB} -rf ${OUTDIR} -th ${THREADS}
./pANI_percentage.py ${PLASMIDS} ${OUTDIR}/pANI.tsv -rf ${OUTBLAST} -i 225

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr ${end_time} - ${start_time}` s.
