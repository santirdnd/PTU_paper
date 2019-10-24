% Escribe un fichero por cada componente conexa de un grafo
function fn = escribe_componentes(H, rootfilename)
    bins = conncomp(H);
    nComp = max(bins);
    fprintf('Hay %d componentes conexas\n', nComp);
    N = hist(bins, nComp);
    [~, I] = sort(N, 'descend');
    
    fn = {};
    for k=1:length(I)
        i = I(k);
        nodos = find(bins == i);
        ff = fillcoef(H.subgraph(nodos));
        mm = matrizcoef(nodos);
        fprintf('Componente: %d, %d nodos, fillcoef %f, matrizcoef: %f, ratio: %f\n', k, N(i), ff, mm, ff/mm);
        filename = sprintf('%s_%d__%d_%d', rootfilename, k, N(i), round(100*ff));
        dlmwrite(filename, H.Nodes.idx(nodos)');
        fn{k} = filename;
    end

end