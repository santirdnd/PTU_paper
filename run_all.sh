#!/usr/bin/env bash

TIME_START=`date +%s`
echo -e "Starting ...\n  `date -d@${TIME_START}`\n"

./download_ncbi_taxonomy.sh
./extract_RefSeq84_database.sh
./generate_protein_seqs.sh plasmid.lst
./extract_plasmid_info.py
./assign_mob_classes.sh plasmid.lst
./assign_pfinder_classes.sh
./list_subgroups.sh
./append_pGroup_annotation.sh
./accnet_RefSeq84.sh plasmid.lst
./ani_RefSeq84.sh
./summarize_pGroups_info.sh > pGroups_181128_summary.txt
./calculate_clusters_density.py ani_RefSeq84/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes13.tsv ani_RefSeq84/RefSeq84_Lani_p50/RefSeq84_ani_p50_links.tsv density_clusters_ani_RefSeq84.txt -i AccessionVersion -c pGroup -s Source -t Target -w ANIp
./calculate_clusters_density.py ani_RefSeq84/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes13.tsv ani_RefSeq84/RefSeq84_Lani_p50/RefSeq84_ani_p50_links.tsv density_clusters_ani_EntbactGrd2.txt -i AccessionVersion -c pGroup -s Source -t Target -w ANIp -f plasmid_NoEnterobacteralesGrd2.lst

TIME_END=`date +%s`
echo -e "\nJob successfully processed.\n  `date -d@${TIME_END}`"
echo "  Execution time was `expr ${TIME_END} - ${TIME_START}` s."

