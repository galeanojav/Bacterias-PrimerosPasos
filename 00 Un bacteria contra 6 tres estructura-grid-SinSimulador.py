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

def creaRed(Nodos,TipoNodos):
    global g,numNodos, numTipoNodos
    numNodos=Nodos
    numTipoNodos=TipoNodos
    g=nx.grid_graph(dim=[numNodos,numNodos], periodic=True)
    for i in g.nodes_iter():
        g.node[i]['tipo']=rd.choice(range(numTipoNodos))
    return g
    
def initialize(numero,tipos):
    global g
    global wr
    global f
    global initialConditions
    global bacteriaStructure   
    initialConditions=0
    # Inicialite file for saving data
    cola= dt.datetime.now().strftime('%Y%m%d%H%M')
    outputfilename = 'competicion_01_{}.csv'.format( cola)
    fileOut = open(outputfilename, 'wb')
    wr = csv.writer(fileOut,quoting = csv.QUOTE_NONE)
    wr.writerow(['Tipo 1','Tipo 2','Tipo 3','Patogeno'])
    f = open( 'competicion_01_{}.ini'.format( cola), "w")
    
    # Crear red    
    g=creaRed(numero,tipos)
    g.pos = nx.spring_layout(g)
    bacteriaStructure=[0,1,2]   
     
def initializeProbabilities():
    global betaMatrix, b_23
    betaMatrix= np.matrix('0 0.2 0.2 0.4; 0.2 0  0.2 0.4;0.2 0.2 0 0.4;0.4 0.4 0.4 0')
    b_modulator=0.5

def creaCmap(N):
    """create a colormap with N  discrete colors"""
    cmap = plt.cm.jet
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # force the first color entry to be grey
    cmaplist[0] = (.2,.4,.5, 1.0)
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    return cmap

def diferencia(listaA,listaB):
    """Los que están en A, pero no en B """
    a=set(listaA)
    b=set(listaB)
    return list(a-b)
   
def observe():
    global initialConditions
    global g,estado,f,numNodos,numTipoNodos
    estado=[]
    contadorAgregado=[]
    cla()
    node_labels={}
    cmapMio=creaCmap(4)
    for i in g.nodes_iter():
        node_labels[i]=g.node[i]['tipo']    
    nx.draw_networkx (g, k=0.8,node_color = [g.node[i]['tipo'] for i in g.nodes_iter()],
            pos = g.pos,cmap=cmapMio, labels=node_labels)
    for i in g.nodes_iter():
        estado.append(g.node[i]['tipo'])
    contador=collections.Counter(estado)
    contadorAgregado=contador.values()
    wr.writerow(contadorAgregado)
    print contadorAgregado
    if initialConditions == 0:
        # Saving data used in simulation, using f of file defined in initialize()
        f.write('GRID de ')
        f.write(str(numNodos)+"\n y tipos de nodos: ")
        f.write(str(numTipoNodos)+"\n")
        f.write(str(contadorAgregado) +"\n")
        f.write('Matrix'+"\n")
        initialConditions=1       
        np.savetxt(f,betaMatrix, fmt='%.4e') 
        f.close()

def update():
    global g    
    try:
        a = rd.choice(g.nodes())
        b = rd.choice(g.neighbors(a))        
        tipoA=g.node[a]['tipo']
        tipoB=g.node[b]['tipo']
        tipoVecino=[]
        aleatorio=random()
        if tipoA in bacteriaStructure:
            #print "Está en la lista",tipoA,tipoB,betaMatrix[tipoA,tipoB]
            for i in g.neighbors(a):
                tipoVecino.append(g.node[i]['tipo'])   
            if diferencia(bacteriaStructure,tipoVecino):
                if aleatorio < betaMatrix[tipoA,tipoB]:  
                    g.node[a]['tipo'] = tipoB                   
            else:
                if aleatorio < b_modulator*betaMatrix[tipoA,tipoB]:            
                    g.node[a]['tipo'] = tipoB
        else:
            if aleatorio < betaMatrix[tipoA,tipoB]:
                g.node[a]['tipo'] = tipoB

    except:
        pass
 #•   g.pos=nx.spring_layout(g,pos=g.pos,iterations=100)   


initializeProbabilities()
initialize(24,6)
for i in range(10000):
    observe()
    update()