import numpy as np


def metric_tensor(cell):
    '''
    Interatomic distance metric tensor, works with any basis
    '''
    # Lattice parameters - unit cell length and angles
    a = cell[0]
    b = cell[1]
    c = cell[2]
    al = np.deg2rad(cell[3])
    be = np.deg2rad(cell[4])
    ga = np.deg2rad(cell[5])

    # Triclinic (universal) Metric Tensor
    g = np.array([[a ** 2, a * b * np.cos(ga), a * c * np.cos(be)],
                  [b * a * np.cos(ga), b ** 2, b * c * np.cos(al)],
                  [c * a * np.cos(be), c * b * np.cos(al), c ** 2]])

    return g


def mt_iad(g, atomA, atomB):
    '''
    Interatomic distance calculated using metric tensor
    Takes two atomic positions
    '''
    # Interatomic distance calculation
    # net vector

    net_vector = atomB - atomA
    # distance matrix multiplication
    distance = np.sqrt((net_vector @ g @ net_vector.transpose()))

    return(distance)
