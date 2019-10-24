#!/usr/bin/env bash

cut -f1 pTUs_kept_190823.tsv | sort | uniq | \
    grep -Ff - graphs_kept_ANIp50/plsm_subgraph_assignment.tsv | \
    ./host_pTU_network.py -

mv host-pTU_links.tsv host-pTU_links_kept_190823.tsv
../append_columns_to_file.py host-pTU_nodes.tsv pTUs_kept_190823.tsv host-pTU_nodes_kept_190823.tsv -ik ID -ek SubGraph -l pTU -d '-'
rm host-pTU_nodes.tsv

# Crear host-pTU_nodes_kept_190823.edit.tsv a partir de host-pTU_nodes_kept_190823.tsv y corregir el rango excesivo de algunos pTU

cut -f1,2 pTUs_kept_190823.tsv > tmp.tsv
../append_columns_to_file.py tmp.tsv host-pTU_nodes_kept_190823.edit.tsv pTUs_kept_190823.tsv -ik SubGraph -ek ID -l Range,Mobilizable,MOB_list -d '-'

cut -f1-3 graphs_kept_ANIp50/plsm_subgraph_assignment.tsv > tmp.tsv
../append_columns_to_file.py tmp.tsv pTUs_kept_190823.tsv plasmid_assignment_kept_190823.tsv -ik SubGraph -ek SubGraph -l pTU,Range,Mobilizable,MOB_list -d '-'

rm tmp.tsv

