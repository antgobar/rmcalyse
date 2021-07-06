
import logging

import numpy as np

logger = logging.getLogger(__name__)

def orthonormalise(positions, m):
    return (m @ positions.T).T

def orthonormalise_distance_to_origin(positions, m):
    ortho = orthonormalise(positions, m)
    return np.power(np.square(ortho).sum(1),0.5)
