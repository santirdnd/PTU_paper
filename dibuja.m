% Dibuja un grafo
function p=dibuja(G, labeltype)
    p=plot(G, 'Layout', 'Force', 'NodeLabel', []);
    
    if nargin > 1
        Et = {};
        
        for i=1:G.numnodes
            if labeltype==1
                Et{i} = sprintf('%d', G.degree(i));
            elseif labeltype==2
                Et{i} = sprintf('%d %s', G.degree(i), G.Nodes.pGroup{i});
            elseif labeltype==3
                Et{i} = sprintf('%d %s %d', G.degree(i), G.Nodes.pGroup{i}, G.Nodes.Size(i));    
            elseif labeltype==4
                Et{i} = sprintf('%d %s %d %s', G.degree(i), G.Nodes.pGroup{i}, G.Nodes.Size(i), string(G.Nodes.AccessionVersion(i)));    
            else
                Et{i} = '*';
            end
        end
        for i=1:length(Et)
            text(p.XData(i),p.YData(i)+0.1, Et(i),'fontsize',16);
        end
    end
end