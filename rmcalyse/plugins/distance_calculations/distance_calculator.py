import numpy as np


def eucledian_distance(coordA, coordB):
    '''
    Calculates distance between two coordinates in an orthnomal basis.
    '''
    distance = np.around((sum((np.array(coordA) - np.array(coordB))**2)**0.5), 4)
    return distance
