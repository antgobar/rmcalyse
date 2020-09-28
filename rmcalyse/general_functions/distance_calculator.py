import numpy as np


def distance_calc(coordA, coordB):
    '''
    Calculates distance between two coordinates in an orthnomal basis.
    '''
    int_dist = np.linalg(np.array(coordA) - np.array(coordB))

    return int_dist
