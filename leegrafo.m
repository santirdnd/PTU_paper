% Lee un grafo de un fichero
function H = leegrafo(filename)
    global G;

    H = G.subgraph(dlmread(filename));
end