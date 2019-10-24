% Dado un grafo, calcula el coeficiente de llenado: 
% el cociente entre el numero de aristas que tiene y las de un clique
% con el mismo numero de vertices
function c = fillcoef(G)
nNodos = height(G.Nodes);
if nNodos == 1
    c = 1;
else
    nEdges = height(G.Edges);
    nClique = nNodos * (nNodos - 1) / 2;
    c = nEdges / nClique;
end
end
