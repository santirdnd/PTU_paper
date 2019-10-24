close all;

% Load previously computed variables
%clear;
%load('vars_EntGdr2.mat');

A = dlmread('matrix_ANIp50_EntGrd2.tsv', '\t');
%for k=1:size(A,1), A(k,k) = 0; end % Este borrado no hace falta, la salida de tsne es similar
W = dlmread('matrix_ANIWF_EntGrd2.tsv', '\t'); W = 100 * W; W(W <= 50) = 0;
F = dlmread('matrix_AF_EntGrd2.tsv', '\t'); F(F <= 50) = 0;
AW = [A W];
AF = [A F];

node = readtable('nodes_EntGrd2.tsv','FileType','text','TextType','string','Format','%s%u%s%s%s%s');
%cats = categories(categorical(node.pGroup));
cats = {'-';'IncB/O/K/Z';'IncC';'IncE1';'IncE10';'IncE11';'IncE12';'IncE13';'IncE14';'IncE15';'IncE16';'IncE17';'IncE18';'IncE19';'IncE2';'IncE20';'IncE21';'IncE22';'IncE23';'IncE24';'IncE25';'IncE26';'IncE27';'IncE28';'IncE3';'IncE4';'IncE5';'IncE6';'IncE7';'IncE8';'IncE9';'IncFE';'IncFK1';'IncFK2';'IncFK3';'IncFS';'IncFSh';'IncFV';'IncFY';'IncHI1A';'IncHI1B';'IncHI2';'IncI1';'IncI2';'IncL/M';'IncN1';'IncN2/3';'IncN3';'IncP1';'IncR1';'IncR2';'IncW';'IncX1';'IncX3';'IncX4';'IncY'};

cmap = [[221 221 204]/255; parula(length(cats)-1)]; % Non assigned pTU '-' => #DDDDCC
for k=1:size(node,1), node.Color(k,:) = cmap(ismember(cats, node.pGroup(k)),:); end

% Convert colormap to hexadecimal RGB and save
%fileID = fopen('pTU_colormap.txt','w');
%for k=1:size(cats)
%    fprintf(fileID, '%s\t#%02X%02X%02X\n', string(cats(k)), uint8(cmap(k,1)*255),uint8(cmap(k,1)*255),uint8(cmap(k,3)*255));
%end
%fclose(fileID);

% Default settings
%rng('default') % for reproducibility
%[TA, lossA] = tsne(A, 'Algorithm','barneshut', 'Distance','euclidean');
%gscatter(TA(:,1), TA(:,2), node.pGroup);

% Best distances seem to be: spearman, correlation, seuclidean, euclidean and cityblock
%rng('default') % for reproducibility
[node.TA, lossA] = tsne(A, 'Algorithm','exact', 'Distance','spearman');
%rng('default') % for reproducibility
[node.TW, lossW] = tsne(W, 'Algorithm','exact', 'Distance','spearman');
%rng('default') % for reproducibility
[node.TF, lossF] = tsne(F, 'Algorithm','exact', 'Distance','spearman');
%rng('default') % for reproducibility
[node.TAW, lossAW] = tsne(AW, 'Algorithm','exact', 'Distance','spearman');
%rng('default') % for reproducibility
[node.TAF, lossAF] = tsne(AF, 'Algorithm','exact', 'Distance','spearman');
%rng('default') % for reproducibility
[node.T3A, loss3A] = tsne(A, 'Algorithm','exact', 'Distance','spearman', 'NumDimensions', 3);

[T, loss] = tsne(A, 'Algorithm','exact', 'Distance','spearman', 'Perplexity',30, 'Exaggeration',6);

% Save variables
%save('vars_EntGdr2.mat','node','lossA','lossW','lossF','lossAW','lossAF','loss3A','cats','cmap');

%
% Graphical representations
%

%gscatter(node.TA(:,1), node.TA(:,2), node.pGroup);
%gscatter(node.TA(:,1), node.TA(:,2), clusterdata(node.TA,'Linkage','ward',75));

figure
hold on
cat = unique(node.pGroup);
for k=1:size(cat)
    scatter(node.TA(node.pGroup==cat(k),1), node.TA(node.pGroup==cat(k),2), 15, node.Color(node.pGroup==cat(k),:), 'filled');
end
legend()
hold off

%s = scatter(node.TA(:,1), node.TA(:,2), 15, node.Color, 'filled');
%text(node.TA(:,1), node.TA(:,2), node.pGroup);
%row = dataTipTextRow('pTU', node.pGroup);
%s.DataTipTemplate.DataTipRows(end+1) = row;
%row = dataTipTextRow('Acc', node.AccessionVersion);
%s.DataTipTemplate.DataTipRows(end+1) = row;

%scatter3(node.T3A(:,1), node.T3A(:,2), node.T3A(:,3), 15, node.Color, 'filled');
%text(node.T3A(:,1), node.T3A(:,2), node.T3A(:,3), node.pGroup);

% Group checking
%cat = unique(node.pGroup);
%for k=1:size(cat)
%    figure
%    scatter(node.TA(node.pGroup==cat(k),1), node.TA(node.pGroup==cat(k),2), 15, 'red', 'filled');
%    hold on
%    text(node.TA(node.pGroup==cat(k),1), node.TA(node.pGroup==cat(k),2), node.pGroup(node.pGroup==cat(k),:));
%    s = scatter(node.TA(:,1), node.TA(:,2), 8, node.Color);
%    row = dataTipTextRow('pTU', node.pGroup);
%    s.DataTipTemplate.DataTipRows(end+1) = row;
%    row = dataTipTextRow('Acc', node.AccessionVersion);
%    s.DataTipTemplate.DataTipRows(end+1) = row;
%end

A = dlmread('matrix_ANIp50_Ent.tsv', '\t');
node = readtable('nodes_Ent.tsv','FileType','text','TextType','string','Format','%s%u%s%s%s%s');
for k=1:size(node,1), node.Color(k,:) = cmap(ismember(cats, node.pGroup(k)),:); end
[node.TA, lossA] = tsne(A, 'Algorithm','exact', 'Distance','spearman');
figure
hold on
cat = unique(node.pGroup);
for k=1:size(cat)
    scatter(node.TA(node.pGroup==cat(k),1), node.TA(node.pGroup==cat(k),2), 15, node.Color(node.pGroup==cat(k),:), 'filled');
end
legend()
hold off

A = dlmread('matrix_ANIp50_kept.tsv', '\t');
node = readtable('nodes_kept.tsv','FileType','text','TextType','string','Format','%s%u%s%s%s%s');
node.pGroup(node.pGroup(:,:)=="Incα",:) = "-";
node.pGroup(node.pGroup(:,:)=="Incβ",:) = "-";
for k=1:size(node,1), node.Color(k,:) = cmap(ismember(cats, node.pGroup(k)),:); end
[node.TA, lossA] = tsne(A, 'Algorithm','exact', 'Distance','spearman');
figure
hold on
cat = unique(node.pGroup);
for k=1:size(cat)
    scatter(node.TA(node.pGroup==cat(k),1), node.TA(node.pGroup==cat(k),2), 15, node.Color(node.pGroup==cat(k),:), 'filled');
end
legend()
hold off
