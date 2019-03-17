import networkx as nx
import numpy as np
import scipy.linalg as la

class Partition(object):
    
    def __init__(self, G, impl):
        self.G = G
        self.impl = impl
    
    def partition(self):
        V = list(self.G.nodes())
        A = V[:len(V)/2]
        V = set(V)
        A = set(A)
        B = V-A
        return A,B
