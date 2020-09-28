import numpy as np
from general_functions import distance_calculator as dc

def centroid_calc(orthonormal_positions, center_atom, orbit_atoms, max_d, coord_no):
    '''
    Takes center_atom e.g. 'Ti', and orbit_atoms e.g. 'Pb', and
    coordination number coord_no (8 for A- and B-site orbitals, 6 for
    O-site.
    Returns atomic coordinates of center atom, centroid (average
    coordinates of orbit atoms) and vector corresponding to the
    relative position of the center atom relative to the centroid.
    '''

    center = []
    orbits = []
    # Script similar to interatomic distance script
    for nC, atom in enumerate(orthonormal_positions):
        if orthonormal_positions[nC][0] in center_atom:
            labelC = orthonormal_positions[nC][:]
            coordC = orthonormal_positions[nC][2:5]
            temp = []  # initialise temporary list for orbits
            for nO, atom in enumerate(orthonormal_positions):
                if orthonormal_positions[nO][0] in orbit_atoms:
                    labelO = orthonormal_positions[nO][:]
                    coordO = orthonormal_positions[nO][2:5]
                    if dc.distance_calc(coordC, coordO) <= max_d:
                        temp.append(labelO)  # append orbits to temp
            if len(temp) == coord_no:
                orbits.append(temp)  # append temp to list of all orbits
                center.append(labelC)  # append center

    centroid_coord_list = []
    # Centroid coordinates (average of orbits)
    for i, orb in enumerate(orbits):
        to_sum = []
        for j in orbits[i]:
            to_sum.append(np.array(j[2:5]))
        centroid_coord = sum(to_sum) / coord_no  # coord_no = coordination number!!!
        centroid_coord_list.append(centroid_coord)

    center_coord = []
    # Coordinates of center atom
    for i in center:
        center_coord.append(np.array(i[2:5]))

    off_centering_vector = []
    # Vector indicating displacement of center atom relative to
    # centroid coordinate
    for i, j in zip(center_coord, centroid_coord_list):
        off_centering_vector.append(np.subtract(i, j))

    return off_centering_vector, centroid_coord_list
