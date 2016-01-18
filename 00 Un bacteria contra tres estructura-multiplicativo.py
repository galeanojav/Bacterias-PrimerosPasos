# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 16:28:51 2015

@author: falevian
"""

import matplotlib
import numpy as np

matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd

import numpy as np

def growth(bacterias,tasas):
    growByType=[]
    for i in range(len(bacterias)):
        growByType.append(np.random.randint(0,bacterias[i]*tasas[i]))
    print growByType
    return growByType

def createNetwork(Nodos,TipoNodos):
    global g,numNodos, numTipoNodos
    numNodos=Nodos
    g=nx.Graph()  
    numTipoNodos=TipoNodos
    #Seed creation
    g=nx.complete_graph(numNodos)
    for i in g.nodes_iter():
        g.node[i]['tipo']=rd.choice(range(numTipoNodos))

    #Growth
    
    return g

def growNetwork(g,numBacterias):
    difBacterias=[]
    numn
    for t in numBacterias:
        g.add_node()
    return g


bacteriaStructure=[0,1,2]   
tasas=[0.5,0.2,0.5,0.5]
numBacterias=[10,20,30,40]
g=createNetwork(20,4)
numBacterias=growth(numBacterias,tasas)
g=growNetwork(g,numBacterias)


#nx.write_gml(g, "test.gml")