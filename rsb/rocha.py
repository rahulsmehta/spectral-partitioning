import networkx as nx
import numpy as np
import scipy.linalg as la

from .partition import Partition

class RochaPartition(Partition):
    def __init__(self, G):
        super(RochaPartition, self).__init__(G, impl='rocha')

    # Return the number of edges crossing the cut (A,B) in G (A,B \subset V)
    def cut_size(self, A, B, G):
        total = 0
        for i,j in G.edges():
            if i in A and j in B:
                total += 1
        return total

    def partition(self):
        G = self.G
        L = nx.laplacian_matrix(G)
        L = L.toarray()
        ev, lv, rv = la.eig(L, left=True, right=True)
        ev = np.real(ev)
        z = zip(ev, rv)
        sorted_eigs = sorted(z, key=lambda t: t[0])
        
        V = set(range(G.number_of_nodes()))
        y = sorted_eigs[1][1]
        x = sorted_eigs[2][1]
        
        ranked_y = sorted(zip(range(len(y)), y), key=lambda t: t[1])
        ranked_y = list(ranked_y)
        A = ranked_y[:int(len(ranked_y)/2)]
        
        A = map(lambda t: t[0], A)
        A = set(A)
        B = V - A
        
        for i in G.nodes():
            d = np.sqrt(x[i]**2 + y[i]**2)
            if d == 0:
                continue
            u = (x[i]/d) * x + (y[i]/d) * y
            ranked_u = sorted(zip(range(len(u)), u), key=lambda t: t[1])
            ranked_u = list(ranked_u)
            R = ranked_u[:int(len(ranked_u)/2)]
            R = map(lambda t: t[0], R)
            R = set(R)
            S = V-R
            if self.cut_size(R,S,G) < self.cut_size(A,B,G):
                print('updating cut, size {}'.format(self.cut_size(R,S,G)))
                A = R
                B = S
        return A,B
