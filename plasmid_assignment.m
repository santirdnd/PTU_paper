% All
% Compila los metadatos de los plásmidos de cada grafo

plasmid_list=cellstr(node.AccessionVersion(:,:));

pTUs = readtable('pTUs_kept_190628.tsv','FileType','text','TextType','string','Format','%s%s');

% Coge todos los ficheros de grafos
lst = dir('0_*');
nFiles = length(lst);

fileID = fopen('plasmid_assignment.tsv' ,'w');
%fprintf(fileID, 'AccessionVersion\tGraphName\tGraphRank\n');
fprintf(fileID, 'AccessionVersion\tpTU\tGraphName\tGraphRank\n');
for k=1:nFiles
    H = leegrafo(lst(k).name);
    for n = 1:height(H.Nodes)
%        fprintf(fileID, '%s\t%s\t%s\n', ...
%                string(H.Nodes.AccessionVersion(n)), ...
%                lst(k).name, ...
%               string(height(H.Nodes)));
        pTU = pTUs.pTU(strcmp(pTUs.GraphName,lst(k).name));
        if isempty(pTU)
            pTU = '-';
        end
        fprintf(fileID, '%s\t%s\t%s\t%s\n', ...
                string(H.Nodes.AccessionVersion(n)), ...
                pTU, ...
                lst(k).name, ...
                string(height(H.Nodes)));
        plasmid_list(strcmp(plasmid_list, H.Nodes.AccessionVersion(n)))=[];
    end
end

for k=1:length(plasmid_list)
%    fprintf(fileID, '%s\t%s\t%s\n', ...
%            string(plasmid_list(k)), ...
%            '-', ...
%            '0');
    fprintf(fileID, '%s\t%s\t%s\t%s\n', ...
            string(plasmid_list(k)), ...
            '-', ...
            '-', ...
            '0');
end

fclose(fileID);
