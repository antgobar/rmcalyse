import numpy as np

def array_distance_orthonormaliser(labels, positions, matrix, center_atom, orbit_atom):
    
    offset = 0.5 # half a unit cell
    
    positions -= offset # now the unit cell goes from -0.5:0.5
    
    # list of indices we're interested in
    idx_of_interest = [i for i,x in enumerate(positions) if labels[i][1] in center_atom]
    idxB = [i for i,x in enumerate(positions) if labels[i][1] in orbit_atom]

    all_distances = []
    center_labels = []
    orbit_labels = []
    
    for index in idx_of_interest:
        
        shifted = (positions[idxB] - positions[index]) # shift all atoms so this one is at the origin
        
        reshuffled = np.mod(shifted + offset, offset * 2) - offset # the clever moving of atoms outside -0.5:0.5
        
        # ORTHONORMALISATION
        orthonormalised = np.dot(matrix, reshuffled.T).T
        
        distances  = np.power(np.square(orthonormalised).sum(1),0.5) # calculate distances
        
        all_distances.append(distances)

        labels_c = [labels[index] for i in range(len(labels[idxB]))]
        labels_o = labels[idxB]

        center_labels.append(labels_c)
        orbit_labels.append(labels_o)

    return all_distances, center_labels, orbit_labels




