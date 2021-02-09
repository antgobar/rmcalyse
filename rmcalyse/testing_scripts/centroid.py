###=====================================================================
### Calculate centroid for atomA orbited by atomB

### ORTHONORMAL DATA TO ANALYSE
from rmc6f_analyse_function_caller import orthonormal_positions
import numpy as np
###=====================================================================


def distance_calc(coordA, coordB):
    '''
    Calculates distance between two coordinates in an orthnomal basis.
    '''
    int_dist = np.around((sum(\
        (np.array(coordA)-np.array(coordB))**2)**0.5),4)
    return(int_dist)


##def interatomic_distance(\
##    orthonormal_positions, atomA, atomB, max_d, min_d = 1):
##    '''
##    Takes in list of atomic coordinates in orthonormal basis.
##    Returns original coordinates and interatomic distances for
##    specified atom pair (atomA atomB).
##    Format: atomA, no, x, y, z, atomB, no, x, y, z, distance between
##    Returns relative coordinates centred on specified atomA.
##    '''
##    
##    int_dist_list = []
##    rel_position = []
##    # Iterate over atoms and calculate distances
##    for nA, atom in enumerate(orthonormal_positions):
##        # Pick 1st atom - Loop and then pick 2nd etx
##        coordA = orthonormal_positions[nA][2:5]
##        labelA = orthonormal_positions[nA][:]
##        for nB, atom in enumerate(orthonormal_positions):
##            # Distance of 1st atoms to all atoms
##            coordB = orthonormal_positions[nB][2:5]
##            ## Check when distance value is called index is [10]!!!
##            labelB = orthonormal_positions[nB][:]
##            distance = distance_calc(coordA, coordB)
##            if distance <= max_d \
##            and distance >= min_d \
##            and orthonormal_positions[nA][0] in atomA \
##            and orthonormal_positions[nB][0] in atomB:
##                ## INTERATOMIC DISTANCE
##                int_dist_list.append(labelA + labelB + [distance])
##                ## COORDINATE DISTANCE relative to atomA
##                rel_position.append(np.array(coordA) - np.array(coordB))
##                temp.append(labelB)
##        centroid_list.append(labelA + temp) 
##    return(int_dist_list, rel_position, centroid_list, temp)
##
##
##distances = interatomic_distance(orthonormal_positions, \
##                                 'Ti', 'O', 3)[0]
##
##print(len(distances))
##print('\n')
##for i in range(10, 27):
##    print(distances[i])
##print('\n')



center_atom = 'Bi'
orbit_atoms = 'Ti'
max_d = 4
coord_no = 8
center = []
orbits = []
for nC, atom in enumerate(orthonormal_positions):
    if orthonormal_positions[nC][0] == center_atom:
        labelC = orthonormal_positions[nC][:]
        coordC = orthonormal_positions[nC][2:5]
        temp = []
        for nO, atom in enumerate(orthonormal_positions):    
            if orthonormal_positions[nO][0] == orbit_atoms:
                labelO = orthonormal_positions[nO][:]
                coordO = orthonormal_positions[nO][2:5]
                if distance_calc(coordC, coordO) < max_d:
                    temp.append(labelO)
        if len(temp) == coord_no:
            orbits.append(temp)
            center.append(labelC)

centroid = []
for i, orb in enumerate(orbits):
    to_sum = []
    for j in orbits[i]:
        to_sum.append(np.array(j[2:5]))
    centroid_coord = sum(to_sum) / coord_no
    centroid.append(centroid_coord)

center_coord = []
for i in center:
    center_coord.append(np.array(i[2:5]))

diff_vector = []
for i, j in zip(center_coord, centroid):
        diff_vector.append(np.subtract(i, j))
print(diff_vector)

#=====================================================================
##from collections import Counter
##
##def centroid(distances, coord):
##    pass
##
##def counter(distances):
##
##    to_count = []
##
##    for n, distance in enumerate(distances):
##        to_count.append(n+distances[n][1])
##        
##        freq = Counter(to_count).values()
##        correct = [i for i in freq if i == 6]
##        
##    return(to_count, freq,correct)
##
##to_count = counter(distances)[0]
##freq = counter(distances)[1]
##correct = counter(distances)[2]
##
##print(to_count, freq, correct, sep = '\n \n')
