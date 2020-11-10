import numpy as np

def orth_iad(atom_list):
    distances = []

    for atom in atom_list:
        # net vector
        v = atom - atom_list
        sq_dist = np.dot(v, v.T)
