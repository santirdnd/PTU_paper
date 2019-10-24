% Dibuja los alineamientos de los grafos

% Coge todos los ficheros de grafos
lst = dir('0_*');
nFiles = length(lst);

for k=1:nFiles
    H = leegrafo(lst(k).name);
    if height(H.Nodes) < 3
        continue
    end
    fileID = fopen(string(lst(k).name)+'.sh' ,'w');
    fprintf(fileID, '#!/usr/bin/env bash\n\n');
    fprintf(fileID, "DATA_FOLDER='../../data'\n\n");
    fprintf(fileID, '~/opt/Easyfig_2.2.2_linux/Easyfig.py \\\n');
    fprintf(fileID, '    -ann_height 150 -blast_height 500 -f1 T -glt 20 -exont 2 \\\n');
    fprintf(fileID, '    -blastn -i 70 \\\n');
    fprintf(fileID, '    -o %s.svg -svg \\\n', string(lst(k).name));
    for n = 1:height(H.Nodes)-1
        fprintf(fileID, '    ${DATA_FOLDER}/%s.gbk \\\n', string(H.Nodes.AccessionVersion(n)));
    end
    fprintf(fileID, '    ${DATA_FOLDER}/%s.gbk\n', string(H.Nodes.AccessionVersion(end)));
    fclose(fileID);
    fileattrib(string(lst(k).name)+'.sh', '+x')
end
