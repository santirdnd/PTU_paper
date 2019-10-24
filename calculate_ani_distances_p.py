#!/usr/bin/env python3

import os
import sys
import re
import shlex
import argparse
import subprocess as sp
import multiprocessing as mp

regex_ok = re.compile(r"^! (One|Two)-way A[AN]I (1|2| ):\s*(\d+\.\d+)% \(SD:\s*(\d+\.\d+)%\), from (\d+) (fragments|proteins)\.$")
regex_error = re.compile(r"^Insuffi.*ent hits to estimate (one|two)-way A[AN]I:\s*(\d+)\.?$")

def perc_calculation(params):
    accno1 = params[0]
    accno2 = params[1]
    hits = params[2]
    cache = params[3]
    ext = params[4]
    dec = params[5]
    window = params[6]
    step = params[7]

    seq1 = os.path.join(cache, accno1+'.'+ext)
    seq2 = os.path.join(cache, accno2+'.'+ext)

    cmd = ['./ani.rb',
               '-1', shlex.quote(seq1),
               '-2', shlex.quote(seq2),
               '-n', shlex.quote(str(hits)),
               '-d', shlex.quote(str(dec)),
               '-w', shlex.quote(str(window)),
               '-s', shlex.quote(str(step)),
               '-t', '1'
          ]
    values = []
    try:
        pc = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE,
                    universal_newlines=True, check=True)
    except sp.CalledProcessError as err:
        if err.returncode < 0:
            raise
    else:
        lines = pc.stdout.strip().splitlines()
        if len(lines) != 3:
            return values
        for idx, line in enumerate(lines):
            m = regex_ok.match(line)
            if m is not None:
                if (idx == 0) and (m.group(1) == 'One') and (m.group(2) == '1'):
                    values.extend(m.group(3, 4, 5))
                elif (idx == 1) and (m.group(1) == 'One') and (m.group(2) == '2'):
                    values.extend(m.group(3, 4, 5))
                elif (idx == 2) and (m.group(1) == 'Two') and (m.group(2) == ' '):
                    values.extend(m.group(3, 4, 5))
                else:
                    values = []
                    break
            else:
                m = regex_error.match(line)
                if m is not None:
                    if ((idx == 0) or (idx == 1)) and (m.group(1) == 'one'):
                        values.extend(('0', '0', m.group(2)))
                    elif (idx == 2) and (m.group(1) == 'two'):
                        values.extend(('0', '0', m.group(2)))
                    else:
                        values = []
                        break
                else:
                    values = []
                    break
        else:
            if len(values) != 9:
                values = []

    return values

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Calculate ANI distances')
    parser.add_argument('accessions', type=str,
                        help='input file with accession numbers')
    parser.add_argument('output', type=str,
                        help='base output name')
    parser.add_argument('seq_cache', type=str,
                        help='subdirectory with sequence files')
    parser.add_argument('-e', '--extension', type=str,
                        default='fna',
                        help='extension of sequence files')
    parser.add_argument('-t', '--threads', type=int,
                        default=1,
                        help='number of parallel threads to be used')
    parser.add_argument('-n', '--hits', type=int,
                        default=50,
                        help='minimum number of hits')
    parser.add_argument('-p', '--perc', type=float,
                        help='minimum (aprox.) shared length of shorter genome')
    parser.add_argument('-d', '--dec', type=int,
                        default=3,
                        help='decimal positions to report')
    parser.add_argument('-w', '--window', type=int,
                        default=1000,
                        help='window length')
    parser.add_argument('-s', '--step', type=int,
                        default=200,
                        help='sliding window step')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    plasmids = []
    pl_size = {}
    with open(args.accessions) as fh:
        for line in fh:
            if line.strip() == '':
                continue
            plasmids.append(line.strip())
            seq_file = os.path.join(args.seq_cache, line.strip()+'.'+args.extension)
            with open(seq_file) as fh_fna:
                next(fh_fna)
                pl_size[line.strip()] = len(next(fh_fna)) - 1

    tasks = []
    threshold = {}
    data = {}
    plasmids_tmp = plasmids[:]
    for p1 in plasmids:
        threshold[p1] = {}
        data[p1] = {}
        for p2 in plasmids_tmp:
            if args.perc:
                core_length = args.perc * min(pl_size[p1], pl_size[p2])
                if core_length <= args.window:
                    threshold[p1][p2] = 1
                else:
                    threshold[p1][p2] = 1 + int((core_length - args.window) // args.step)
            else:
                threshold[p1][p2] = args.hits
            tasks.append([p1, p2, threshold[p1][p2], args.seq_cache, \
                          args.extension, args.dec, args.window, args.step])
            data[p1][p2] = None
        plasmids_tmp.remove(p1)

    headers = ('Query genome', 'Reference genome', \
               'Query size', 'Reference size', 'min_hits', \
               'ANI_o1', 'ANI_o1_SD', 'ANI_o1_frag', \
               'ANI_o2', 'ANI_o2_SD', 'ANI_o2_frag', \
               'ANI_tw', 'ANI_tw_SD', 'ANI_tw_frag')
    if os.path.isfile(args.output):
        with open(args.output) as fh:
            header_line = next(fh).strip()
            if header_line != '\t'.join(headers):
                print('Wrong header:', header_line, file=sys.stderr)
                sys.exit(1)
            for line in fh:
                if line.strip() == '':
                    continue
                if (line[-1] != '\n') or (len(line.strip().split('\t')) != len(headers)):
                    print('Bad formatted line:', line, file=sys.stderr)
                    sys.exit(1)
                p1, p2, leftover = line.strip().split('\t', 2)
                if (p1 not in plasmids) or (p2 not in plasmids):
                    print('Wrong list of plasmids:', p1, p2, file=sys.stderr)
                    continue
                if data[p1][p2] != None:
                    print('Duplicatted line:', line, file=sys.stderr)
                else:
                    for idx, t in enumerate(tasks):
                        if (t[0] == p1) and (t[1] == p2):
                            tasks.pop(idx)
                            break
                    else:
                        print('Orphan task:', p1, p2, file=sys.stderr)
                        sys.exit(1)
                data[p1][p2] = leftover.split('\t', 3)[3]

    total = len(plasmids)**2
    processed = total - len(tasks)
    print('Processing {0:d} plasmids => {1:d} comparisons'.format(len(plasmids), total), file=sys.stderr)
    print('\t{0:d} ({1:.2%}) already calculated'.format(processed, processed/total), file=sys.stderr)

    pool_size = args.threads
    with mp.Pool(processes = pool_size) as pool:
        outputs = pool.map(perc_calculation, tasks)
        pool.close()
        pool.join()

    for t, o in zip(tasks, outputs):
        data[t[0]][t[1]] = '\t'.join(o)

    with open(args.output, 'w') as fh:
        fh.write('\t'.join(headers)+'\n')
        for p1 in data:
            for p2 in data[p1]:
                if len(data[p1][p2]) == 0:
                    print('Warning: Error calculating ANI for', p1, '=>', p2, file=sys.stderr)
                    continue
                items = (p1, p2, str(pl_size[p1]), str(pl_size[p2]),
                         str(threshold[p1][p2]), data[p1][p2])
                fh.write('\t'.join(items)+'\n')

