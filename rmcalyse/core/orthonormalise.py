import numpy as np

def orthonormalise(cell, atom_list):
    '''
    Function which returns orthonormalised coordinates from 
    cell parameters and list of atomic positions in any basis
    args:
        cell: 
            cell side lengths a, b, c
            cell angle alpha, beta, gamma
        atom_list:
            list of atomic positions
            current column format ['Atom', 'no.', 'x.', 'y', 'z']
    '''

    atom_list_head = ['Atom', 'no.', 'x.', 'y', 'z']
    # Lattice parameters - unit cell length and angles
    a = cell[0]
    b = cell[1]
    c = cell[2]

    al = np.deg2rad(cell[3])
    be = np.deg2rad(cell[4])
    ga = np.deg2rad(cell[5])

    V = a*b*c * (1 - np.cos(al)**2 - np.cos(be)**2 - \
    np.cos(ga)**2 + 2*np.cos(al)*np.cos(be)*np.cos(ga))**0.5

    #Converion to orthonormal
    a1 = a
    a2 = 0
    a3 = 0

    b1 = b * np.cos(ga)
    b2 = b * np.sin(ga)
    b3 = 0

    c1 = c * np.cos(be)
    c2 = c * (np.cos(al) - (np.cos(be) * np.cos(ga))) / np.sin(ga)
    c3 = V / (a * b * np.sin(ga))

    M = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])

    ## Orthonormal real position function "@" symbol is matrix mult
    ## Not sure if it works everywhere
    def ortho_position(atom):
        orth_pos = np.around(((M @ atom.transpose()).transpose()), 4)
        list_pos = np.array(orth_pos).ravel().tolist()
        return(list_pos)

    # Initialise ortho position list
    orthonormal_positions = []

    # Iterate over atoms and calculate orthonormal positions
    for n, atom in enumerate(atom_list):
        atom = np.array([atom_list[n][2:5]])
        label = atom_list[n][:2]
        atomI = ortho_position(atom)
        orthonormal_positions.append(label + atomI)

##    print('\nFormat of atom orthonormalised list \
##    (coordinates are REAL, not fractional): ', atom_list_head,\
##      orthonormal_positions[0], sep = '\n')
    
    return(orthonormal_positions)

def orth_xyz(orthonormal_positions):
    '''
    Split orthonormal positions into x, y and z columns. Will be useful
    at some point...
    '''
    orth_x = []
    orth_y = []
    orth_z = []
    for n, atom in enumerate(orthonormal_positions):
        o_p = orthonormal_positions
        label = o_p[n][:2]
        orth_x.append(label + [o_p[n][2]])
        orth_y.append(label + [o_p[n][3]])
        orth_z.append(label + [o_p[n][4]])

    return orth_x, orth_y, orth_x
