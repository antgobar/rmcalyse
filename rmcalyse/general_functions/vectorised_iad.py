import numpy as np

def iad_mt(cell, atom_list):
    '''
    Interatomic distance metric tensor
    '''
    # Lattice parameters - unit cell length and angles
    a = cell[0]
    b = cell[1]
    c = cell[2]

    al = np.deg2rad(cell[3])
    be = np.deg2rad(cell[4])
    ga = np.deg2rad(cell[5])

    # Triclinic (universal) Metric Tensor
    g=np.array([[a ** 2, a * b * np.cos(ga), a * c * np.cos(be)],
                [b * a * np.cos(ga),b ** 2 , b * c * np.cos(al)],
                [c * a * np.cos(be), c * b * np.cos(al), c ** 2]])

    # Interatomic distance function
    distance_list = []
    for atom in atom_list:
        net_v = np.array(atom) - np.array(atom_list) # Net vector
        distance = np.sqrt(np.dot(net_v.T, net_v))
        reduced_distance_matrix = np.diagonal(distance)

        distance_list.append(reduced_distance_matrix)

    return np.array(distance_list)


