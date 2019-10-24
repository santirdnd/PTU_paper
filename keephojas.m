% Coge todos los ficheros de grafos y extrae los que son hojas de la
% jerarquia
lst = dir('0_*');
nFiles = length(lst);

nombre = {};
% nvertices = zeros(nFiles, 1);
% fillcoef = zeros(nFiles, 1);
for k=1:nFiles
    tmp = split(lst(k).name, '__');
    nombre{k} = tmp{1};
    % Las tres lineas siguientes para sacar una lista de n y fillcoef
    % tmp = split(tmp{2}, '_');
    % nvertices(k) = str2double(tmp{1});
    % fillcoef(k) = str2double(tmp{2});
end

hoja = zeros(nFiles, 1);

for k=1:nFiles
    path = strcat(nombre{k}, '_');
    if sum(startsWith(nombre, path)) == 0
        hoja(k) = 1;
    end
end

% Borramos los que no son hojas
for k =1:nFiles
    if hoja(k) == 0
        delete(lst(k).name);
    end
end

% nombre(hoja == 1)
% {lst(hoja==1).name}