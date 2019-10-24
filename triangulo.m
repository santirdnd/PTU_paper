% Devuelve un vector con las componentes en la parte por encima de la
% diagonal principal de una matriz cuadrada
function v = triangulo(A)
m = size(A, 1);
N = m*(m+1) / 2;
v = [];
for k = 1:m-1
    v = [v; diag(A, k)];
end
end