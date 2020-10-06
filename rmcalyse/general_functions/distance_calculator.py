import numpy as np


def distance_calc(coordA, coordB):
    '''
    Calculates distance between two coordinates in an orthnomal basis.
    '''
    int_dist = np.around((sum(
        (np.array(coordA) - np.array(coordB))**2)**0.5), 4)
    return int_dist
