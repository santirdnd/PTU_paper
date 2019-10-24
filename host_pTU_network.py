#!/usr/bin/env python3

import os
import sys
import csv
import argparse

parser = argparse.ArgumentParser(
    description='Create host-pTU bipartite network')
parser.add_argument('input', type=argparse.FileType('r'),
                    help='input data file')
parser.add_argument('-n', '--nodes', type=str,
                    default='host-pTU_nodes.tsv',
                    help='nodes network file')
parser.add_argument('-l', '--links', type=str,
                    default='host-pTU_links.tsv',
                    help='links network file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

pTU_lst = {}
species_lst = {}

reader = csv.DictReader(args.input, delimiter='\t')

with open(args.links, 'w') as fh_links:
    line = '\t'.join(('Source', 'Target', 'Weigth', 'Type'))
    fh_links.write(line+'\n')
    for row in reader:
        pTU = row['SubGraph']
        species = row['TaxSpecies']
        line = '\t'.join((pTU, species, '1', 'Undirected'))
        fh_links.write(line+'\n')

        if pTU not in pTU_lst:
            pTU_lst[pTU] = {'SubGraph': row['SubGraph'], \
                            'MOB_list': {row['MOB_60']: 1}, \
                            'Range': 1, \
                            'TaxPhylum': row['TaxPhylum'], \
                            'TaxClass': row['TaxClass'], \
                            'TaxOrder': row['TaxOrder'], \
                            'TaxFamily': row['TaxFamily'], \
                            'TaxGenus': row['TaxGenus'], \
                            'TaxSpecies': row['TaxSpecies']}
        else:
            if pTU_lst[pTU]['SubGraph'] != row['SubGraph']:
                print('Warning:', pTU, pTU_lst[pTU]['SubGraph'], row['SubGraph'])
            if row['MOB_60'] not in pTU_lst[pTU]['MOB_list']:
               pTU_lst[pTU]['MOB_list'][row['MOB_60']] = 1
            else:
               pTU_lst[pTU]['MOB_list'][row['MOB_60']] = pTU_lst[pTU]['MOB_list'][row['MOB_60']] + 1
            # Al final en realidad han quedado como if..else pero se puede dar una vuelta mas a la logica
            if pTU_lst[pTU]['Range'] <= 6:
                if pTU_lst[pTU]['TaxPhylum'] != row['TaxPhylum']:
                    pTU_lst[pTU]['Range'] = 6
                    pTU_lst[pTU]['TaxPhylum'] = '*'
                    pTU_lst[pTU]['TaxClass'] = '*'
                    pTU_lst[pTU]['TaxOrder'] = '*'
                    pTU_lst[pTU]['TaxFamily'] = '*'
                    pTU_lst[pTU]['TaxGenus'] = '*'
                    pTU_lst[pTU]['TaxSpecies'] = '*'
                elif pTU_lst[pTU]['TaxClass'] != row['TaxClass']:
                    pTU_lst[pTU]['Range'] = 6
                    pTU_lst[pTU]['TaxClass'] = '*'
                    pTU_lst[pTU]['TaxOrder'] = '*'
                    pTU_lst[pTU]['TaxFamily'] = '*'
                    pTU_lst[pTU]['TaxGenus'] = '*'
                    pTU_lst[pTU]['TaxSpecies'] = '*'
            if pTU_lst[pTU]['Range'] < 5:
                if pTU_lst[pTU]['TaxOrder'] != row['TaxOrder']:
                    pTU_lst[pTU]['Range'] = 5
                    pTU_lst[pTU]['TaxOrder'] = '*'
                    pTU_lst[pTU]['TaxFamily'] = '*'
                    pTU_lst[pTU]['TaxGenus'] = '*'
                    pTU_lst[pTU]['TaxSpecies'] = '*'
            if pTU_lst[pTU]['Range'] < 4:
                if pTU_lst[pTU]['TaxFamily'] != row['TaxFamily']:
                    pTU_lst[pTU]['Range'] = 4
                    pTU_lst[pTU]['TaxFamily'] = '*'
                    pTU_lst[pTU]['TaxGenus'] = '*'
                    pTU_lst[pTU]['TaxSpecies'] = '*'
            if pTU_lst[pTU]['Range'] < 3:
                if pTU_lst[pTU]['TaxGenus'] != row['TaxGenus']:
                    pTU_lst[pTU]['Range'] = 3
                    pTU_lst[pTU]['TaxGenus'] = '*'
                    pTU_lst[pTU]['TaxSpecies'] = '*'
            if pTU_lst[pTU]['Range'] < 2:
                if pTU_lst[pTU]['TaxSpecies'] != row['TaxSpecies']:
                    pTU_lst[pTU]['Range'] = 2
                    pTU_lst[pTU]['TaxSpecies'] = '*'
        if species not in species_lst:
            species_lst[species] = {'TaxPhylum': row['TaxPhylum'], \
                                    'TaxClass': row['TaxClass'], \
                                    'TaxOrder': row['TaxOrder'], \
                                    'TaxFamily': row['TaxFamily'], \
                                    'TaxGenus': row['TaxGenus'], \
                                    'TaxSpecies': row['TaxSpecies']}

with open(args.nodes, 'w') as fh_nodes:
    line = '\t'.join(('ID', 'Type', 'SubGraph', 'Mobilizable', 'MOB_list', 'Range', 'TaxPhylum', 'TaxClass', 'TaxOrder', 'TaxFamily', 'TaxGenus', 'TaxSpecies'))
    fh_nodes.write(line+'\n')
    pTU_pad = '\t'.join(('-',)*4)
    for item in pTU_lst:
        if len(pTU_lst[item]['MOB_list']) > 1:
            Mobilizable = 'Mobilizable'
        elif list(pTU_lst[item]['MOB_list'])[0] != '-':
            Mobilizable = 'Mobilizable'
        else:
            Mobilizable = 'NonMobilizable'
        line='\t'.join((item, 'pTU', \
                        pTU_lst[item]['SubGraph'], \
                        Mobilizable, \
                        ', '.join(["'{0}': {1}".format(k, v) for k,v in pTU_lst[item]['MOB_list'].items()]), \
                        str(pTU_lst[item]['Range']), \
                        pTU_lst[item]['TaxPhylum'], \
                        pTU_lst[item]['TaxClass'], \
                        pTU_lst[item]['TaxOrder'], \
                        pTU_lst[item]['TaxFamily'], \
                        pTU_lst[item]['TaxGenus'], \
                        pTU_lst[item]['TaxSpecies']))
        fh_nodes.write(line+'\n')
    for item in species_lst:
        line='\t'.join((item, 'Host', \
                        pTU_pad, \
                        species_lst[item]['TaxPhylum'], \
                        species_lst[item]['TaxClass'], \
                        species_lst[item]['TaxOrder'], \
                        species_lst[item]['TaxFamily'], \
                        species_lst[item]['TaxGenus'], \
                        species_lst[item]['TaxSpecies']))
        fh_nodes.write(line+'\n')

