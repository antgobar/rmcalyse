# ------------------------------------------------------------------------
###
# Program/module to calculate interatomic distances
# From orthonormal distances coordinates only
###
###
# Example of how to call this module
###
### import interatomic_distance as i_d
###
### i_a_dist_list = i_d.interatomic_distance(op, 'Sr', ['Ti', 'Nb'], 4, 1)[0]
###
# ------------------------------------------------------------------------

import numpy as np

from general_functions import distance_calculator as dc


def interatomic_distance(orthonormal_positions,
                         atomA,
                         atomB,
                         min_d,
                         max_d):
    '''
    Takes in list of atomic coordinates in orthonormal basis.
    Returns original coordinates and interatomic distances for
    specified atom pair (atomA atomB).
    !!Format: atomA, no, x, y, z, atomB, no, x, y, z, distance between!!
    Returns relative coordinates centred on specified atomA.
    '''

    int_dist_list = []
    rel_position = []

    # Iterate over atoms and calculate distances
    for nA, atom in enumerate(orthonormal_positions):
        # Pick 1st atom - Loop and then pick 2nd etx
        if orthonormal_positions[nA][0] in atomA:
            coordA = orthonormal_positions[nA][2:5]
            labelA = orthonormal_positions[nA][:]

            for nB, atom in enumerate(orthonormal_positions):
                # Distance of 1st atoms to all atoms
                if orthonormal_positions[nB][0] in atomB:
                    coordB = orthonormal_positions[nB][2:5]
                    labelB = orthonormal_positions[nB][:]
                    distance = dc.distance_calc(coordA, coordB)
                    if distance <= max_d \
                            and distance >= min_d:

                            # INTERATOMIC DISTANCE
                        int_dist_list.append(labelA + labelB +
                                             [distance])
                        # COORDINATE DISTANCE relative to atomA
                        rel_position.append(np.array(coordA) -
                                            np.array(coordB))

    return int_dist_list, rel_position
