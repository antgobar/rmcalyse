def array_distance_orthonormaliser(position_labels, raw_positions):
    
    positions = np.array([x for x in raw_positions]) # want a numpy array of the positions
    offset = 0.5 # half a unit cell (helpfully it's cubic so don't need anything more complex than this)
    positions -= offset # now the unit cell goes from -19 to 19
    idx_of_interest = [i for i,x in enumerate(raw_positions) if position_labels[i][1] in center_atom] # hack to find a list of indices we're interested in
    results = np.zeros((positions.shape[0],3)) # predefine results array for speed
    all_distances = []

    t0 = time.perf_counter()
    for i in idx_of_interest:
        shifted = (positions - positions[i]) #shift all atoms so this one is at the origin
        reshuffled = np.mod(shifted+offset, offset*2)-offset # the clever moving of atoms outside -19:19 back
        orth_resh = np.dot(rmc_data.matrix, reshuffled.T).T
        distances  = np.power(np.square(orth_resh).sum(1),0.5) # calculate distances
        idx = np.argsort(distances) # returns an array of sorted indices (i.e. distances[idx[0]] = 0, the distance from the atom to itself, distances[idx[1]] is somewthing like 2.5, etc.
        results[i,:] = -np.mean(orth_resh[idx[1:7], :],0) #note we start at 1 to avoid the 0 for the same atom. Then average them. this calculates the central point so the displacements vector is -ve this
        all_distances.append(distances)
    runtime = round(time.perf_counter() - t0, 5)
    print(f'total time taken {runtime} s')
    return distances

distances_yo = array_distance_orthonormaliser(position_labels, rmc_data.raw_basis_positions)