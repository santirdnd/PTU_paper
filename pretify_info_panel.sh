#!/usr/bin/env bash

patch -p0 -i $1

CONFFILE=network/config.json

sed -i .bak 's/"pgroup",/"pGroup",/g' ${CONFFILE}
sed -i .bak 's/"mob_60",/"MOBscan (60%)",/g' ${CONFFILE}
sed -i .bak 's/"taxgenus",/"Genus",/g' ${CONFFILE}
rm ${CONFFILE}.bak

DATAFILE=network/data.json

#sed -i .bak 's/"accessionversion":"\([[:alnum:]_.]\)"/"Accession Number":"<a href=\\"https:\/\/www.ncbi.nlm.nih.gov\/nuccore\/\1\\" target=\\"_blank\\">\1<\/a>"/g' ${DATAFILE}
sed -i .bak 's/"accessionversion":/"Accession Number":/g' ${DATAFILE}
sed -i .bak 's/"organismname":/"Organism Name":/g' ${DATAFILE}
sed -i .bak 's/"pgroup":/"pGroup":/g' ${DATAFILE}
sed -i .bak 's/"mob_60":/"MOBscan (60%)":/g' ${DATAFILE}
sed -i .bak 's/"mob_70":/"MOBscan (70%)":/g' ${DATAFILE}
sed -i .bak 's/"pfinder_95":/"PlasmidFinder (95%)":/g' ${DATAFILE}
sed -i .bak 's/"pfinder_95abrv":/"PF_95":/g' ${DATAFILE}
sed -i .bak 's/"pfinder_80":/"PlasmidFinder (80%)":/g' ${DATAFILE}
sed -i .bak 's/"pfinder_80abrv":/"PF_80":/g' ${DATAFILE}
sed -i .bak 's/"size":"/"Size":"/g' ${DATAFILE}
sed -i .bak 's/"taxspecies":/"Especies":/g' ${DATAFILE}
sed -i .bak 's/"taxgenus":/"Genus":/g' ${DATAFILE}
sed -i .bak 's/"taxfamily":/"Family":/g' ${DATAFILE}
sed -i .bak 's/"taxorder":/"Order":/g' ${DATAFILE}
sed -i .bak 's/"taxclass":/"Class":/g' ${DATAFILE}
sed -i .bak 's/"taxphylum":/"Phylum":/g' ${DATAFILE}
sed -i .bak 's/"taxsuperkingdom":/"Superkingdom":/g' ${DATAFILE}
rm ${DATAFILE}.bak

