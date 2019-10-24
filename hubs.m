% Dado un grafo, devuelve los indices de los hubs, los nodos que al
% quitarlos producen componentes conexas disjuntas
function idx = hubs(G)
nNodos = height(G.Nodes);
idx = [];

for i=1:nNodos
    H = rmnode(G, i);
    b = conncomp(H);
    nc = length(unique(b));
    if nc > 1
        idx = [idx; i];
    end
end

end