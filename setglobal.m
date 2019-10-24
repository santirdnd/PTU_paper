% Declaracion de variables globales
global node A G
% Leemos el fichero de nodos, con estructura:
% AccessionVersion Size MOB_60 PFinder_80 pGroup Filtered
node = tdfread('nodes.tsv');
%node = tdfread('../nodes_kept.tsv');

% Leemos la matriz de distancias
% Podemos utilizar la ANIWF o la ANIp50:
% A = dlmread('matrix_ANIWF.tsv', '\t');
% G = graph((A > 0.5) & (A < 1));
%
A = dlmread('matrix_ANIp50.tsv', '\t'); % Entre 0 y 100 %, realmente 0, 69--100
%A = dlmread('../matrix_ANIp50_kept.tsv', '\t');
%
% Borramos la diagonal
A = A - diag(diag(A));
%
G = graph(A > 50);
%
% Anadimos una etiqueta a los nodos con el indice original
G.Nodes.idx = [1:size(A,1)]';
% Anadimos el Size
G.Nodes.Size = node.Size;
% Anadimos el pGroup
G.Nodes.pGroup = cellstr(node.pGroup);
% Anadimos el AccessionVersion
G.Nodes.AccessionVersion = cellstr(node.AccessionVersion);
%
% Codificamos las distintas posibilidades del MOB_60
tmp = cellstr(node.MOB_60);
MOB_60 = unique(tmp);
G.Nodes.MOB_60 = repmat(-1, length(tmp), 1);
for k=2:length(MOB_60)
    G.Nodes.MOB_60(strcmp(tmp, MOB_60(k))) = k-1;
end
%
% Codificamos las distintas posibilidades del pGroup
tmp = cellstr(node.pGroup);
pGroup = unique(tmp);
G.Nodes.pGroupIdx = repmat(-1, length(tmp), 1);
for k=2:length(pGroup)
    G.Nodes.pGroupIdx(strcmp(tmp, pGroup(k))) = k-1;
end
%
% Creamos el fichero con todos los indices del grafo global
dlmwrite('0', G.Nodes.idx');
%
% Borramos lo que sobra
clear k tmp;