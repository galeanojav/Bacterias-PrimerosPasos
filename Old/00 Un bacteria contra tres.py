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
import pycxsimulator
import numpy as np
import csv
import datetime as dt 
import os.path



def initialize():
    global g
    global wr
    global f
    global initialConditions
    initialConditions=0
    # Inicialite file for saving data
    cola= dt.datetime.now().strftime('%H%M')
    outputfilename = 'competicion_01_{}.csv'.format( cola)
    fileOut = open(outputfilename, 'w')
    wr = csv.writer(fileOut,quoting = csv.QUOTE_NONE)
    wr.writerow(['Tipo 1','Tipo 2','Tipo 3','Patogeno'])
    f = open( 'competicion_01_{}.ini'.format( cola), "w")
    
 #   g = nx.karate_club_graph()
    g=nx.powerlaw_cluster_graph(100,3,0.3)
    g.pos = nx.spring_layout(g)

    for i in g.nodes_iter():
        if random() < .33:
            g.node[i]['tipo'] = 0
        elif random() < .33:
            g.node[i]['tipo'] = 1
        elif random() < .33:
            g.node[i]['tipo'] = 2
        elif random() < .33:
            g.node[i]['tipo'] = 3
        else:
            g.node[i]['tipo'] = 4
            


def creaCmap(N):
    """create a colormap with N  discrete colors"""
    cmap = plt.cm.jet
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # force the first color entry to be grey
    cmaplist[0] = (.2,.4,.5, 1.0)
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    return cmap

# def update3to4():
  
    
def observe():
    global initialConditions
    global g,estado,f
    estado=[]
    contadorAgregado=[]
    cla()
    node_labels={}
    cmapMio=creaCmap(5)
    for i in g.nodes_iter():
        node_labels[i]=g.node[i]['tipo']    
    nx.draw_networkx (g, k=0.8,node_color = [g.node[i]['tipo'] for i in g.nodes_iter()],
            pos = g.pos,cmap=cmapMio, labels=node_labels)
    for i in g.nodes_iter():
        estado.append(g.node[i]['tipo'])
    contador=collections.Counter(estado)
    contadorAgregado=[contador[0],contador[1],contador[2]+contador[3],contador[4]]
    print contadorAgregado
    wr.writerow(contadorAgregado)
    if initialConditions == 0:
        # Saving data if the simulation, using f defined in initialize()
        f.write('Tipo 1' + 'Tipo 2'+'Tipo 3'+'Patogeno' +"\n")
        f.write(str(contadorAgregado) +"\n")
        f.write('Matrix'+"\n")
        initialConditions=1       
        np.savetxt(f,betaMatrix, fmt='%.4e') 
        f.close()

def initializeProbabilities():
    global betaMatrix 
    betaMatrix= np.matrix('0 0 0 0 0.8; 0 0 0 0 0.8;0 0 0 0.8 0.8;0 0 0 0 0.8;0.4 0.4 0.4 0.4 0')

def update():
    global g
    global betaMatrix
    a = rd.choice(g.nodes())
    try:
        b = rd.choice(g.neighbors(a))
        tipoA=g.node[a]['tipo']
        tipoB=g.node[b]['tipo']
        if random() < betaMatrix[tipoA,tipoB]:
            g.node[a]['tipo'] = tipoB
     #        g.node[a]['tipo'] = tipoB if random() < betaMatrix[tipoA,tipoB]
        elif g.node[a]['tipo']==2:
            if 0 in [g.node[i]['tipo']  for i in g.neighbors(a)] and 1  in [g.node[i]['tipo'] for i in g.neighbors(a)]:
                if  random() < betaMatrix[2,3]:               
                    g.node[a]['tipo'] = 3
    except:
        pass
 #•   g.pos=nx.spring_layout(g,pos=g.pos,iterations=100)   


initializeProbabilities()
pycxsimulator.GUI().start(func=[initialize, observe, update])