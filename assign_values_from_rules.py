#!/usr/bin/env python3

import os
import sys
import csv
import argparse

parser = argparse.ArgumentParser(
    description='Assign new data field as per rules config.')
parser.add_argument('input', type=argparse.FileType('r'),
                    help='input file')
parser.add_argument('rules', type=argparse.FileType('r'),
                    help='rules file, specific ones should be first')
parser.add_argument('output', type=argparse.FileType('w'),
                    help='output file')
parser.add_argument('-k', '--key', type=str,
                    help='column name to use as key')
parser.add_argument('-l', '--label', type=str,
                    help='header label for new data column')
parser.add_argument('-d', '--default', type=str,
                    default='',
                    help='default value for unassigned data')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

rules=[]
for line in args.rules:
    if line.strip() == '':
        continue
    items = line.strip().split('\t')
    if len(items) < 3:
        print('Error: Wrong rule format:', line.strip(), file=sys.stderr)
        sys.exit(1)
    rules.append(items)

reader = csv.DictReader(args.input, delimiter='\t')

key_column = ''
if args.key:
    if args.key in reader.fieldnames:
        key_column = args.key
    else:
        print('Error: Invalid key:', args.key, file=sys.stderr)
        sys.exit(1)
else:
    key_column = reader.fieldnames[0]

if args.label:
    args.output.write(key_column+'\t'+args.label+'\n')

for row in reader:
    for rule in rules:
        if row[rule[0]] == rule[1]:
            field = rule[2]
            break
    else:
        field = args.default

    args.output.write(row[key_column]+'\t'+field+'\n')
