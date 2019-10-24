#!/bin/bash

start_time=`date +%s`
echo 'Starting ...'
date

OUTDIR=ani_RefSeq84
DATADIR=original
COLORDIR=color_rules
PLASMIDS=plasmid.lst
METADATA=plasmid_mob_pfinder_filt_pTU.tsv

mkdir -p $OUTDIR

#./calculate_ani_distances_p.py -t 50 -p 0.5 $PLASMIDS $OUTDIR/RefSeq84_ani_p50.tsv $DATADIR
#cp $OUTDIR/RefSeq84_ani_p50.tsv $OUTDIR/RefSeq84_ani_p50_orig.tsv
#grep -vFf plasmid_bad.lst $OUTDIR/RefSeq84_ani_p50_orig.tsv > $OUTDIR/RefSeq84_ani_p50.tsv
#./genome_similarity_network.py $OUTDIR/RefSeq84_ani_p50.tsv ANI_tw $OUTDIR/RefSeq84_Lani_p50
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes.tsv $METADATA $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes2.tsv -ik ID -ek AccessionVersion -l AccessionVersion,MoleculeType,SeqName,Size,TaxSuperkingdom,TaxPhylum,TaxClass,TaxOrder,TaxFamily,TaxGenus,TaxSpecies,OrganismName,MOB_60,MOB_70,PFinder_80,PFinder_80smpl,PFinder_95,PFinder_95smpl,pTU_Manual,pTU_PID,HRange,Mobilizable -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes2.tsv $COLORDIR/plasmid_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color -d '#000000'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes2.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes3.tsv -ik ID -ek ID -l Color -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes3.tsv $COLORDIR/mob60_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_MOB60 -d '#000000'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes3.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes4.tsv -ik ID -ek ID -l Color_MOB60 -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes3.tsv $COLORDIR/mob70_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_MOB70 -d '#000000'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes4.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes5.tsv -ik ID -ek ID -l Color_MOB70 -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes5.tsv $COLORDIR/skingdom_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Superkingdom -d '#000000'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes5.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes6.tsv -ik ID -ek ID -l Color_Superkingdom -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes6.tsv $COLORDIR/phylum_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Phylum -d '#999999'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes6.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes7.tsv -ik ID -ek ID -l Color_Phylum -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes7.tsv $COLORDIR/ani_class_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Class -d '#CAB2D6'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes7.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes8.tsv -ik ID -ek ID -l Color_Class -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes8.tsv $COLORDIR/ani_order_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Order -d '#D9D9D9'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes8.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes9.tsv -ik ID -ek ID -l Color_Order -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes9.tsv $COLORDIR/ani_family_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Family -d '#D9D9D9'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes9.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes10.tsv -ik ID -ek ID -l Color_Family -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes10.tsv $COLORDIR/ani_genus_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Genus -d '#999999'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes10.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes11.tsv -ik ID -ek ID -l Color_Genus -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes11.tsv $COLORDIR/ani_genus_ent_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_Genus_Ent -d '#999999'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes11.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes12.tsv -ik ID -ek ID -l Color_Genus_Ent -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes12.tsv $COLORDIR/pfamily_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_pFamily -d '#DDDDCC'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes12.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes13.tsv -ik ID -ek ID -l Color_pFamily -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes13.tsv $COLORDIR/ptuPID_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_pTU_PID -d '#DDDDCC'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes13.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes14.tsv -ik ID -ek ID -l Color_pTU_PID -d '-'
./assign_values_from_rules.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes14.tsv $COLORDIR/hrange_color_rules.tsv $COLORDIR/tmp_colors.tsv -k ID -l Color_HRange -d '#DDDDCC'
./append_columns_to_file.py $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes14.tsv $COLORDIR/tmp_colors.tsv $OUTDIR/RefSeq84_Lani_p50/RefSeq84_ani_p50_nodes15.tsv -ik ID -ek ID -l Color_HRange -d '-'

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.
