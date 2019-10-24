#!/usr/bin/env python3

import os
import sys
import csv
import argparse

parser = argparse.ArgumentParser(
    description='Append data columns to text file')
parser.add_argument('input', type=argparse.FileType('r'),
                    help='input data file')
parser.add_argument('extra', type=argparse.FileType('r'),
                    help='extra data file')
parser.add_argument('output', type=argparse.FileType('w'),
                    help='output data file')
parser.add_argument('-ik', '--input_label_key', type=str,
                    default='ID',
                    help='label to use as key for input data file')
parser.add_argument('-ek', '--extra_label_key', type=str,
                    default='ID',
                    help='label to use as key for extra data file')
parser.add_argument('-l', '--new_labels', type=str,
                    help='comma separated label list for new info from extra data file')
parser.add_argument('-d', '--default', type=str,
                    default='',
                    help='default value for unassigned rows')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

data = {}
reader_extra = csv.DictReader(args.extra, delimiter='\t')
if args.extra_label_key not in reader_extra.fieldnames:
    print('Error: Invalid extra file key:', args.extra_label_key, file=sys.stderr)
    sys.exit(1)
if args.new_labels:
    new_labels = args.new_labels.split(',')
    for item in new_labels:
        if item not in reader_extra.fieldnames:
            print('Error: Invalid extra file label:', item, file=sys.stderr)
            sys.exit(1)
else:
    new_labels = []
    for item in reader_extra.fieldnames:
        if item != args.extra_label_key:
            new_labels.append(item)
for row in reader_extra:
    data[row[args.extra_label_key]] = []
    for item in new_labels:
        data[row[args.extra_label_key]].append(row[item])

reader_input = csv.DictReader(args.input, delimiter='\t')
if args.input_label_key not in reader_input.fieldnames:
    print('Error: Invalid input file key:', args.input_label_key, file=sys.stderr)
    sys.exit(1)
fields = []
fields.extend(reader_input.fieldnames)
fields.extend(new_labels)
args.output.write('\t'.join(fields)+'\n')
for row in reader_input:
    items = []
    for item in reader_input.fieldnames:
        items.append(row[item])
    if row[args.input_label_key] in data:
        items.extend(data[row[args.input_label_key]])
    else:
        items.extend([args.default]*len(new_labels))
    args.output.write('\t'.join(items)+'\n')
