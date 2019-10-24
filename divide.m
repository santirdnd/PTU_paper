% Divide un grafo en componentes conexas
% Utiliza sucesivamente las siguientes opciones:
%   i) Mira si ya tiene mas de una componente
%  ii) Quita los nodos que separan el grafo en componentes
% iii) Quita los nodos aislados
function divide(H, raiz)
    if (height(H.Nodes) < 10) || (fillcoef(H) > 0.9)
        return;
    end
    

    nComp = max(conncomp(H));
    if nComp > 1
        fn = escribe_componentes(H, raiz);
        for k=1:length(fn)
            tmp = split(fn{k}, '__');
            divide(leegrafo(fn{k}), tmp{1});
        end
        return;
    end
    
    idx = hubs(H);
    if ~isempty(idx)
        H = rmnode(H, idx);
        divide(H, raiz);
        return;
    end
    
    idx = isolatedneig(H);
    if ~isempty(idx)
        H = rmnode(H, idx);
        divide(H, raiz);
    end

end