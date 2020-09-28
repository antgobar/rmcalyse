###------------------------------------------------------------------------
###
### Program/module to calculate interatomic distances 
### From orthonormal distances coordinates only
###
###
### Example of how to call this module
###
### import interatomic_distance as i_d
###
### i_a_dist_list = i_d.interatomic_distance('Sr', ['Ti', 'Nb'], 4, 1)[0]
###
###------------------------------------------------------------------------

import numpy as np


def distance_calc(coordA, coordB):
    int_dist = np.around((sum((np.array(coordA)-np.array(coordB))**2)**0.5),3)
    return(int_dist)


def interatomic_distance(orthonormal_positions, atomA, atomB, max_d, min_d = 1):

    interatomic_distance_list = []
    relative_position = []

    # Iterate over atoms and calculate distances
    for nA, atom in enumerate(orthonormal_positions):
        # Pick 1st atom - Loop and then pick 2nd etx
        coordA = orthonormal_positions[nA][2:5]
        labelA = orthonormal_positions[nA][:2]

        for nB, atom in enumerate(orthonormal_positions):
            # Distance of 1st atoms to all atoms
            coordB = orthonormal_positions[nB][2:5]
            labelB = orthonormal_positions[nB][:2]
            distance = distance_calc(coordA, coordB)

            if distance <= max_d \
            and distance >= min_d \
            and orthonormal_positions[nA][0] in atomA \
            and orthonormal_positions[nB][0] in atomB:
            # Make sure you're selecting the correct atoms edit as needed
                # Interatomic distance for selected atoms
                interatomic_distance_list.append(labelA + labelB + [distance])
                # relative position (for cell 'collapse' function)
                relative_position.append(np.array(coordA) - np.array(coordB))

    return(interatomic_distance_list, relative_position)
