# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 11:50:57 2015

@author: t148444
"""
import networkx as nx
import random as rd

def creaRed(numNodes,gradoMedio):
    g=nx.Graph()
    
    for i in range(numNodes):
        g.add_node(i)
        if rd.random() < .33:
                g.node[i]['tipo'] = 0
        elif rd.random() < .33:
            g.node[i]['tipo'] = 1
        elif rd.random() < .33:
            g.node[i]['tipo'] = 2
        else:
            g.node[i]['tipo'] = 3
    
    for i in range(gradoMedio*numNodes):
         a = rd.choice(g.nodes())
         b = rd.choice(g.nodes())
         if not g.node[a]['tipo'] == 3:
             if not g.node[b]['tipo'] == 3:
                 if rd.random()<0.8:
                     g.add_edge(a,b)
             else:
                 if rd.random()<0.3:
                     g.add_edge(a,b)
         else:
             if rd.random()<0.3:
                     g.add_edge(a,b)
    return max(nx.connected_component_subgraphs(g), key=len)
    
g=creaRed(100,3)
node_labels={}             
for i in g.nodes_iter():
        node_labels[i]=g.node[i]['tipo']    
nx.draw_networkx (g, k=0.8,labels=node_labels)                 

