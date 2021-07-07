import numpy as np


def orthonormal_iad(orthonormal_positions):
    '''
    Calculates distance between each element in list of orthonormal positions
    using matrix multiplication
    Only works in orthonormal basis
    '''
    distances = []

    for position in orthonormal_positions:
        # loop through each atom in list
        net_vector = position - orthonormal_positions
        # matrix mult atom with all atoms
        # results are squared distances in a symmetric matrix
        squared_dist = np.dot(net_vector, net_vector.T)
        # make distances positive and square root
        abs_distance = np.sqrt(np.sqrt(squared_dist ** 2))
        # matrix is symmetric, only take diagonal
        distance = np.diagonal(abs_distance)
        distances.append(distance)

    return distances
