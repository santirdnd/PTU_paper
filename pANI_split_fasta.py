#!/usr/bin/env python2

import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='split fasta in fragments')
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='source table file')
parser.add_argument('-seq', '--sequencesfolder', nargs='?', type=str, default='.',
		    help='sequence files folder')
parser.add_argument('-w', '--window', nargs='?', type=int, default=250,
		    help='window size')
parser.add_argument('-s', '--step', nargs='?', type=int, default=50,
		    help='sliding step size')
parser.add_argument('-sf', '--splitfolder', nargs='?', type=str, default='splits',
		    help='split files folder')
args = parser.parse_args()

def split(filename,window,step,splitfolder):

    queryfile=open(filename,'r')
    for line in queryfile:
        if line.startswith('>'):
            head1,resto=line.split(' ',1)
        else:
            seq=line
            
    nameout=splitfolder+'/'+head1[1:]+'_sp'+str(window)+'_'+str(step)+'.fna'
    fragfile=open(nameout,'w')
    i=1

    while len(seq)/window>0:
        frag=seq[0:window]
        seq=seq[step:]
        fragfile.write(head1+'_'+str(i)+'\n'+frag+'\n')
        i=i+1

    fragfile.close()

#os.mkdir(args.splitfolder)

for line in args.infile:
    fl=os.path.join(args.sequencesfolder, line.strip()+'.fna')
    split(fl,args.window,args.step,args.splitfolder)
    
