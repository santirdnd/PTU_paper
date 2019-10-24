% Dado un conjunto de indices (filas y columnas) devuelve
% el valor medio de la parte triangular superior de la submatriz
function m = matrizcoef(idx)
    global A
    
    m = mean(triangulo(A(idx, idx)));
end