#!/usr/bin/env python2

import os
import sys
import argparse
import subprocess as sp
import multiprocessing as mp

def exeBLAST(params):
    query=args.queryfolder+'/'+params+args.extension
    ofname=args.rstfolder+'/'+params+'.b6'
    of=open(ofname,'w')
    fmt="6 qseqid sseqid nident pident positive ppos mismatch gapopen gaps length qstart qend sstart send evalue bitscore"

    for db in databases:
        data=args.dbfolder+'/'+db
        #out=params+'.tmp'
        out=args.rstfolder+'/'+params+'.tmp'
#        sp.call(['blastn', '-db', db, '-query', query,'-out', of, '-outfmt',fmt])
#        sp.call(['blastn', '-db', db, '-query', query,'-out', of, '-max_hsps', '1', '-outfmt',fmt])
        sp.call(['blastn', '-db', data, '-query', query,'-out',out, '-max_hsps', '1', '-outfmt',fmt])
        fh=open(out,'r')
	for line in fh:
            of.write(line)
    os.remove(out)

    of.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run blast for list')
    parser.add_argument('querylist', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='source table file')
    parser.add_argument('queryfolder', nargs='?', type=str, default='splits',
                        help='query folder with split sequences')
    parser.add_argument('-ext','--extension', nargs='?', type=str, default='_sp250_50.fna',
                        help='window defining extension')
    parser.add_argument('-df', '--dbfolder', nargs='?', type=str, default='plasmiddb',
                        help='database folder')
    parser.add_argument('-rf', '--rstfolder', nargs='?', type=str, default='results',
                        help='results folder')
    parser.add_argument('-th', '--threads', nargs='?', type=int, default=4,
                        help='number of threads')

    args = parser.parse_args()


    if not os.path.exists(args.rstfolder):
        os.mkdir(args.rstfolder)

    databases=[]
    tasks=[]
    for line in args.querylist:
        tasks.append(line.strip())
        databases.append(line.strip())

    pool_size=args.threads
    pool= mp.Pool(pool_size)
    pool.map(exeBLAST,tasks)
