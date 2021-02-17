import numpy as np
from plugins.distance_calculations import distance_calculator

def get_centroids(orthonormal_positions,
                  center_atom,
                  orbit_atoms,
                  max_distance,
                  coordination_number):
    '''
    Function which returns the list of vectors described by the distance
    between a given atom and the centroid of the polyhedra defined by
    its nearest neighbours

    Arguments:
        orthonormal_positions:
            list of lists of atom (element), atom_id and x, y, z
            orthonormal coordinates
            list format: [element, atom_id, x, y, z]
        center_atom:
            chosen atom from which to calculate distance vector do
            centroid
        orbit_atoms:
            chosen atom from which to form polyhedra and calculate
            centroid position
        max_distance:
            maximum interatomic distance window to look for nearest
            neighbour atom
        coordination_number:
            coordination number of center_atom and orbit_atoms pairs
            examples assume persovskite cnofiguration
            e.g. 1
                center_atom: A-site
                orbit_atom: B-site
                coordination_number: 8
            e.g. 2
                center_atom: B-site
                orbit_atom: O-site
                coordination_number: 6
            e.g. 3
                center_atom: A-site
                orbit_atom: O-site
                coordination_number: 12                
    
    returns list of vectors describing the distance between the central atom
    and the centroid position, and returns a list of centroid coordinates
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
                    if distance_calculator.eucledian_distance(coordC, coordO) <= max_distance:
                        temp.append(labelO)  # append orbits to temp
            if len(temp) == coordination_number:
                orbits.append(temp)  # append temp to list of all orbits
                center.append(labelC)  # append center

    centroid_positions = []
    # Centroid coordinates (average of orbits)
    for i, orb in enumerate(orbits):
        to_sum = []
        for j in orbits[i]:
            to_sum.append(np.array(j[2:5]))
        centroid_coord = sum(to_sum) / coordination_number
        centroid_positions.append(centroid_coord)

    center_coord = []
    # Coordinates of center atom
    for i in center:
        center_coord.append(np.array(i[2:5]))

    off_centering_vector = []
    # Vector indicating displacement of center atom relative to
    # centroid coordinate
    for i, j in zip(center_coord, centroid_positions):
        off_centering_vector.append(np.subtract(i, j))

    # vertical stack into one numpy array
    # e.g. select x coordinates: off_centering_vector[: ,0]
    off_centering_vector = np.vstack(off_centering_vector)

    return off_centering_vector, centroid_positions
