% Devuelve los indices de los puntos aislados del grafo (aquellos cuya
% distancia al mas proximo es mayor que el doble de la distancia media)
function idx = isolatedneig(H)
    p = dibuja(H);
    x = p.XData;
    y = p.YData;
    np = length(x);
    
    dmin = zeros(np, 1);
    dmax = zeros(np, 1);
    for i = 1:np
        neig = neighbors(H, i);
        dx = x(neig) - x(i);
        dy = y(neig) - y(i);
        dist = sqrt(dx .* dx + dy .* dy);
        dmin(i) = min(dist);
        dmax(i) = max(dist);
    end
    dmin = normalize(dmin);
    dmax = normalize(dmax);
    
    % plot(1:np, dmin, 'b', 1:np, dmax, 'r');
  
    idx = find( ( (dmin > 2) | (dmax > 2) )  & (degree(H) > 1) );
end