#!/usr/bin/env bash

start_time=`date +%s`
echo 'Starting ...'
date

# Missannotated Salmonella enterica subsp. enterica serovar Quebec str. S-1267 chromosome
echo 'NZ_CP022019.1' > plasmid_bad.lst
# NG_* accession numbers are for CDSs, not plasmids
awk -F"\t" '$3 ~ /NG_/ { print $3 }' plasmid_mob.tsv >> plasmid_bad.lst
# Append missassembled PacBIO internal control sequence
echo 'NZ_CP013938.1' >> plasmid_bad.lst
echo 'NZ_CP020583.1' >> plasmid_bad.lst
echo 'NZ_CP020935.1' >> plasmid_bad.lst
echo 'NZ_CP021055.1' >> plasmid_bad.lst
echo 'NZ_CP021993.1' >> plasmid_bad.lst
echo 'NZ_CP022430.1' >> plasmid_bad.lst
echo 'NZ_CP022493.1' >> plasmid_bad.lst
echo 'NZ_CP022496.1' >> plasmid_bad.lst
# Append manually curated list of hyperconnected small "plasmids" (lenght < 20kb and grade => 70)
echo 'NC_025014.1' >> plasmid_bad.lst  # Escherichia coli F plasmid traD gene
echo 'NC_025157.1' >> plasmid_bad.lst  # Origin of replication of plasmid colE1 and immunity region
echo 'NC_005248.1' >> plasmid_bad.lst  #
echo 'NC_008352.1' >> plasmid_bad.lst  #
echo 'NC_008439.1' >> plasmid_bad.lst  #
echo 'NC_009345.1' >> plasmid_bad.lst  #
echo 'NC_010072.1' >> plasmid_bad.lst  #
echo 'NC_010896.1' >> plasmid_bad.lst  #
echo 'NC_011511.1' >> plasmid_bad.lst  #
echo 'NC_011513.1' >> plasmid_bad.lst  #
echo 'NC_011602.1' >> plasmid_bad.lst  #
echo 'NC_016137.1' >> plasmid_bad.lst  #
echo 'NC_017329.1' >> plasmid_bad.lst  #
echo 'NC_019060.1' >> plasmid_bad.lst  #
echo 'NC_022376.1' >> plasmid_bad.lst  #
echo 'NC_025195.1' >> plasmid_bad.lst  #
echo 'NC_032098.1' >> plasmid_bad.lst  #
echo 'NZ_CP007485.1' >> plasmid_bad.lst  #
echo 'NZ_CP010832.1' >> plasmid_bad.lst  #
echo 'NZ_CP011333.1' >> plasmid_bad.lst  #
echo 'NZ_CP011335.1' >> plasmid_bad.lst  #
echo 'NZ_CP011336.1' >> plasmid_bad.lst  #
echo 'NZ_CP011337.1' >> plasmid_bad.lst  #
echo 'NZ_CP011573.1' >> plasmid_bad.lst  #
echo 'NZ_CP011626.1' >> plasmid_bad.lst  #
echo 'NZ_CP011638.1' >> plasmid_bad.lst  #
echo 'NZ_CP013143.1' >> plasmid_bad.lst  #
echo 'NZ_CP014087.1' >> plasmid_bad.lst  #
echo 'NZ_CP014097.1' >> plasmid_bad.lst  #
echo 'NZ_CP014100.1' >> plasmid_bad.lst  #
echo 'NZ_CP014101.1' >> plasmid_bad.lst  #
echo 'NZ_CP018981.1' >> plasmid_bad.lst  #
echo 'NZ_CP019138.1' >> plasmid_bad.lst  #
echo 'NZ_CP019692.1' >> plasmid_bad.lst  #

grep -vf plasmid_bad.lst plasmid.lst > plasmid_kept.lst

awk -F"\t" '$18 == "Enterobacterales" { print $3 }' plasmid_mob.tsv | grep -vf plasmid_bad.lst > plasmid_Enterobacterales.lst
awk -F"\t" '$20 == "Escherichia" { print $3 }' plasmid_mob.tsv | grep -vf plasmid_bad.lst > plasmid_Escherichia.lst

echo 'Job successfully processed.'
end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.
