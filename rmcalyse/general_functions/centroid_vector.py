import numpy as np
from general_functions import distance_calculator as dc


def centroid_calc(orthonormal_positions,
                  center_atom,
                  orbit_atoms,
                  max_d,
                  coord_no):
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
        max_d:
            maximum interatomic distance window to look for nearest
            neighbour atom
        coord_no:
            coordination number of center_atom and orbit_atoms pairs
            examples assume persovskite cnofiguration
            e.g. 1
                center_atom: A-site
                orbit_atom: B-site
                coord_no: 8
            e.g. 2
                center_atom: B-site
                orbit_atom: O-site
                coord_no: 6
            e.g. 3
                center_atom: A-site
                orbit_atom: O-site
                coord_no: 12                
    
    returns list of vectors describing the distance between the central atom
    and the centroid position, and returns a list of centroid coordinates
    '''
    import time
    center = []
    orbits = []
    t0 = time.perf_counter()
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
    
    
    # deans messing about here, doesn't alter the output, just makes it take longer :)
    t1 = time.perf_counter()
    positions = np.array([x[2:] for x in orthonormal_positions]) # want a numpy array of the positions
    offset = 39.3399/2 # half a unit cell (helpfully it's cubic so don't need anything more complex than this)
    positions -= offset # now the unit cell goes from -19 to 19
    idx_of_interest = [i for i,x in enumerate(orthonormal_positions) if x[0] in center_atom] # hack to find a list of indices we're interested in
    results = np.zeros((positions.shape[0],3)) # predefine results array for speed
    for i in idx_of_interest:
        shifted = (positions - positions[i]) #shift all atoms so this one is at the origin
        reshuffled = np.mod(shifted+offset, offset*2)-offset # the clever moving of atoms outside -19:19 back
        distances  = np.power(np.square(reshuffled).sum(1),0.5) # calculate distances
        idx = np.argsort(distances) # returns an array of sorted indices (i.e. distances[idx[0]] = 0, the distance from the atom to itself, distances[idx[1]] is somewthing like 2.5, etc.
        results[i,:] = -np.mean(reshuffled[idx[1:7], :],0) #note we start at 1 to avoid the 0 for the same atom. Then average them. this calculates the central point so the displacements vector is -ve this

    t2 = time.perf_counter()

    print('first time was {}'.format(t1-t0))
    print('first time was {}'.format(t2-t1))





    return off_centering_vector, centroid_coord_list
