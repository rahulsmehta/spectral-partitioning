import networkx as nx
import numpy as np
import scipy.linalg as la

# Return the number of edges crossing the cut (A,B) in G (A,B \subset V)
def E(A,B,G):
    total = 0
    for i,j in G.edges():
        if i in A and j in B:
            total += 1
    return total

def rocha_partition(G, eps=1e-10):
    L = nx.laplacian_matrix(G)
    L = L.toarray()
    ev, lv, rv = la.eig(L, left=True, right=True)
    ev = np.real(ev)
    ev = list(map(adjust_eps, ev))
    z = zip(ev, rv)
    sorted_eigs = sorted(z, key=lambda t: t[0])
    
    V = set(range(G.number_of_nodes()))
    y = sorted_eigs[1][1]
    x = sorted_eigs[2][1]
    
    ranked_y = sorted(zip(range(len(y)), y), key=lambda t: t[1])
    A = ranked_y[:len(ranked_y)/2]
    
    A = map(lambda t: t[0], A)
    A = set(A)
    B = V - A
    
    for i in G.nodes():
        u = x[i]/np.sqrt(x[i]**2 + y[i]**2)*x + y[i]/np.sqrt(x[i]**2 + y[i]**2) * y
        ranked_u = sorted(zip(range(len(u)), u), key=lambda t: t[1])
        R = ranked_u[:len(ranked_u)/2]
        R = map(lambda t: t[0], R)
        R = set(R)
        S = V-R
        
        if E(R,S,G) < E(A,B,G):
            A = R
            B = S
            
    return A,B
