import networkx as nx
import numpy as np
import scipy.linalg as la

def feidler_vector(G, eps=1e-10):
    L = nx.laplacian_matrix(G)
    L = L.toarray()
    ev, lv, rv = la.eig(L, left=True, right=True)
    ev = np.real(ev)
    ev = list(map(adjust_eps, ev))
    z = zip(ev, rv)
    sorted_eigs = sorted(z, key=lambda t: t[0])
    min_ev = min(ev)
    new_evs = filter(lambda x: x != min_ev, sorted(ev))
    l2 = list(new_evs)[0]
    second_vector = list(filter(lambda t: t[0] == l2, sorted_eigs))[0]
    return l2, second_vector

# TODO: Not implemented
def partition(G, k):
    raise
        