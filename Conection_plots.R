setwd("~/Documentos/violines")
conection_species <- read.delim("~/Documentos/violines/trajectory_species.tsv")
conection_families <- read.delim("~/Documentos/violines/trajectory_family.tsv")
conection_orders <- read.delim("~/Documentos/violines/trajectory_order.tsv")
conection_classes <- read.delim("~/Documentos/violines/trajectory_class.tsv")
conection_phyla <- read.delim("~/Documentos/violines/trajectory_phylum.tsv")


#VIOLINES
library(vioplot)

vioplot(conection_species$Diff_Host_Trajectory_Percentaje,conection_families$Diff_Host_Trajectory_Percentaje,conection_orders$Diff_Host_Trajectory_Percentaje,conection_classes$Diff_Host_Trajectory_Percentaje,conection_phyla$Diff_Host_Trajectory_Percentaje,  names = c('Species','Families','Orders','Classes','Phyla'),col = 'steel blue')


#BARRAS
library(ggplot2)
conections <- read.delim("~/Documentos/violines/conection_globalnumbers.tsv")

conections$Taxa<-factor(conections$Taxa, levels = conections$Taxa[order(-conections$Cluster)])

ggplot(data=conections, aes(x=Taxa, y= Cluster))+ ylab('Taxa connecting cluster ratio')+
  geom_bar(stat='identity',fill='steel blue')+
  #theme_minimal() +
  theme(panel.background =element_rect(fill = 'white', colour = 'black', size = 1), panel.grid = element_blank(),axis.title.y=element_text(size=14),axis.title.x =element_blank(), axis.line = element_blank(), axis.text = element_text(size = 12, color = 'black'))

conections$Taxa<-factor(conections$Taxa, levels = conections$Taxa[order(-conections$Plasmid)])

ggplot(data=conections, aes(x=Taxa, y= Plasmid))+ ylab('Plasmids with inter-taxa connection ratio')+
  geom_bar(stat='identity',fill='steel blue')+
  #theme_minimal() +
  theme(panel.background =element_rect(fill = 'white', colour = 'black', size = 1), panel.grid = element_blank(),axis.title.y=element_text(size=14),axis.title.x =element_blank(), axis.line = element_blank(), axis.text = element_text(size = 12, color = 'black'))
