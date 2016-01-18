# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 16:28:51 2015

@author: falevian
"""

import matplotlib

matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import collections

def initialize():
    global g
 #   g = nx.karate_club_graph()
    g=nx.powerlaw_cluster_graph(100,3,0.3)
    g.pos = nx.spring_layout(g)
    for i in g.nodes_iter():
        if random() < .3:
            g.node[i]['state'] = 1
        elif random() < .3:
            g.node[i]['state'] = 2
        elif random() < .3:
            g.node[i]['state'] = 3
        else:
            g.node[i]['state'] = 0

def creaCmap(N):
    """create a colormap with N  discrete colors"""
    cmap = plt.cm.jet
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # force the first color entry to be grey
    cmaplist[0] = (.2,.4,.5,1.0)
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    return cmap

    
def observe():
    global g,estado
    estado=[]
    cla()
    node_labels={}
    cmapMio=creaCmap(4)
    for i in g.nodes_iter():
        node_labels[i]=g.node[i]['state']    
    nx.draw_networkx (g, k=0.8,node_color = [g.node[i]['state'] for i in g.nodes_iter()],
            pos = g.pos,cmap=cmapMio, labels=node_labels)
    for i in g.nodes_iter():
        estado.append(g.node[i]['state'])
    contador=collections.Counter(estado)
    print contador.get(0),';',contador.get(1),';',contador.get(2),';',contador.get(3)


p_i1 = 0.5 # infection probability S -> I3
p_i2 = 0.7 # infection probability S -> I2
p_i3 = 0.1 # infection probability I1 -> I2
p_i4 = 0.8 # infection probability I2 -> I1
p_r  = 0.3 # recovery probability
p_d=0.1 # removing probability

def update():
    global g
    a = rd.choice(g.nodes())
    try:
        if g.node[a]['state'] == 0: # if susceptible
            b = rd.choice(g.neighbors(a))
            if g.node[b]['state'] == 1: # if neighbor b is infected by virus 1
                g.node[a]['state'] = 1 if random() < p_i1 else 0
            elif g.node[b]['state'] == 2: # if neighbor b is infected by virus 2
                g.node[a]['state'] = 2 if random() < p_i2 else 0
            elif g.node[b]['state'] == 3:
                g.node[a]['state'] = 1 if random() < p_i1 else 0
                g.node[a]['state'] = 2 if random() < p_i2 else 0
        elif g.node[a]['state'] == 1:   #if infected by Virus 1
            b = rd.choice(g.neighbors(a))
            if g.node[b]['state'] == 2 or g.node[b]['state'] == 3: # if neighbor b is infected virus 2 or 1 and 2
                g.node[a]['state'] = 3 if random() < p_i3 else 1 
                g.node[a]['state'] = 0 if random() < p_r else 1
        elif g.node[a]['state'] == 2:    #if infected by Virus 2
            b = rd.choice(g.neighbors(a))
            if g.node[b]['state'] == 1 or g.node[b]['state'] == 3: # if neighbor b is infected virus 1 or 1 and 2
                g.node[a]['state'] = 3 if random() < p_i4 else 2 
                g.node[a]['state'] = 0 if random() < p_r else 2
        elif g.node[a]['state'] == 3:    #if infected by Virus 2 and 3
                g.node[a]['state'] = 2 if random() < p_r else 3
                g.node[a]['state'] = 1 if random() < p_r else 3
                if random() < p_d:
                    g.remove_node(a)
        
    except:
        pass
 #   g.pos=nx.spring_layout(g,pos=g.pos,iterations=100)   


import pycxsimulator

pycxsimulator.GUI().start(func=[initialize, observe, update])