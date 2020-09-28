###=====================================================================
###---------------------------------------------------------------------
###
###     RMCAlyse apha by A.G.B & W.S. - all functions
###
###     Called by rmc6f_analyse_function_caller.py
###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###             COPY AND PASTE THIS AND WRITE FUNCTION WITHIN



###
###---------------------------------------------------------------------
###=====================================================================

import os
import re           # look through text file for relevant data
import numpy as np
import time
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

###=====================================================================
###---------------------------------------------------------------------
###                     READ FILE

def read_in(file_in):

    '''
    Reads in *.rmc6f file from the read_in directory and extracts useful
    parametere e.g. unit cell parameters and atomic positions
    '''

    cwd = os.getcwd()
    read_in_path = cwd + '/read_in/'


    rmc6f_input = open(read_in_path + file_in, 'r')

    line_elements = []
    line_density = []
    line_supercell = []
    line_cell =[]
    line_atom_list = []

##    print('\nReading file:', file_in, '...')

    # Extract and save variables
    for line in rmc6f_input:
            #	header
            if line.find('Atom types present:') >= 0:
                line_elements = line
            if line.find('Number density') >= 0:
                line_density = line
            if line.find('Supercell') >= 0:
                line_supercell = line
            if line.find('Cell') >= 0:
                line_cell = line
            #	atom lines
            if line.find('[1]') >= 0:
                    line_atom_list.append(line)


    # Close file! 
    rmc6f_input.close()
##    print('\nFile is closed: ', rmc6f_input.closed)

    # Put element, atom no. and atomic positions into lists
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_elements)   ### FIX
    elements = [float(i) for i in temp]                     ### FIX
    temp = re.findall('\d+\.\d+', line_density)
    density = [float(i) for i in temp]
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell)
    supercell = [int(i) for i in temp]
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
    cell = [float(i) for i in temp] # Needed for interatomic distances

    atom_list = []
    for line in line_atom_list:
            temp = []
            temp_1 = re.findall(r'\b\d+\b', line)       #	ints
            temp_2 = re.findall('[a-zA-Z]+', line)  	#	letters
            temp_3 = re.findall('\d+\.\d+', line)   	#	floats
            temp.append(temp_2[0])
            temp.append(int(temp_1[0]))
            temp.append(float(temp_3[0]))
            temp.append(float(temp_3[1]))
            temp.append(float(temp_3[2]))
            atom_list.append(temp)

    atom_list_head = ['Atom', 'no.', 'x.', 'y', 'z']
##    print('\nFormat of atom list (non orthonormalised): ',\
##        atom_list_head, atom_list[0], sep = '\n')

    return(cell, atom_list, elements, supercell, density)

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                     ORTHONORMALISE ATOMIC COORDINATES

def orthonormalise(cell, atom_list):
    '''
    Takes in cell parameters and list of atoms and fractional
    atomic coordinates from *.rmc6f file.
    Outputs orthonormalised coordinates
    Format: atom, no, x, y, z
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

    return(orth_x, orth_y, orth_x)

###                         
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                     INTERATOMIC DISTANCE

def distance_calc(coordA, coordB):
    '''
    Calculates distance between two coordinates in an orthnomal basis.
    '''
    int_dist = np.around((sum(\
        (np.array(coordA)-np.array(coordB))**2)**0.5),4)
    return(int_dist)


def interatomic_distance(\
    orthonormal_positions, atomA, atomB, max_d, min_d = 1):
    '''
    Takes in list of atomic coordinates in orthonormal basis.
    Returns original coordinates and interatomic distances for
    specified atom pair (atomA atomB).
    Format: atomA, no, x, y, z, atomB, no, x, y, z, distance between
    Returns relative coordinates centred on specified atomA.
    '''
    
    int_dist_list = []
    rel_position = []

    # Iterate over atoms and calculate distances
    for nA, atom in enumerate(orthonormal_positions):
        # Pick 1st atom - Loop and then pick 2nd etx
        coordA = orthonormal_positions[nA][2:5]
        labelA = orthonormal_positions[nA][:]

        for nB, atom in enumerate(orthonormal_positions):
            # Distance of 1st atoms to all atoms
            coordB = orthonormal_positions[nB][2:5]
            ## Check when distance value is called index is [10]!!!
            labelB = orthonormal_positions[nB][:]
            distance = distance_calc(coordA, coordB)
            if distance <= max_d \
            and distance >= min_d \
            and orthonormal_positions[nA][0] in atomA \
            and orthonormal_positions[nB][0] in atomB:
                ## INTERATOMIC DISTANCE
                int_dist_list.append(labelA + labelB + [distance])
                ## COORDINATE DISTANCE relative to atomA
                rel_position.append(np.array(coordA) - np.array(coordB))
               
    return(int_dist_list, rel_position)

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###             CENTROID CALCULATION

def centroid(orthonormal_positions, center_atom, orbit_atoms, max_d, coord_no):
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

    centroid_list = []
    ## Centroid coordinates (average of orbits)
    for i, orb in enumerate(orbits):
        to_sum = []
        for j in orbits[i]:
            to_sum.append(np.array(j[2:5]))
        centroid_coord = sum(to_sum) / coord_no
        centroid_list.append(centroid_coord)

    center_coord = []
    ## Coordinates of center atom
    for i in center:
        center_coord.append(np.array(i[2:5]))

    diff_vector = []
    ## Vector indicating displacement of center atom relative to
    ## centroid coordinate
    for i, j in zip(center_coord, centroid_list):
            diff_vector.append(np.subtract(i, j))

    return(diff_vector, center_coord, centroid_list)

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                         AVERAGE CELL PARAMETER
 
def av_unit_cell(orthonormal_positions, atom):
    '''
    Takes in list of atomic coordinates in orthonormal basis.
    Returns average nearest neighbour distance for specified atom.
    '''

    cell_param_list = interatomic_distance(orthonormal_positions,\
                                               atom, atom, 4.5, 1)[0]
    # Cell parameters to be averaged
    to_ave = []
    
    for dist, i in enumerate(cell_param_list):
            val = cell_param_list[dist][10]
            to_ave.append(val)
        
    av_cell_param = np.around(np.average(to_ave), 4)

    return(av_cell_param)

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                         FRACITONAL COORDINATE CELL
 
def frac_coord(orthonormal_positions, av_cell_param):
    '''
    Takes in list of atomic coordinates in orthonormal basis
    and a desired cell parameter for cell normalisation.
    Returns fractional coordinates relative to average cell parameter.
    '''

    frac_pos= []

    for n, atom in enumerate(orthonormal_positions):
        frac_pos.append(np.around((np.array(\
            orthonormal_positions[n][2:])/av_cell_param), 4))

    return(frac_pos)

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                         PLOT RELATIVE POSITIONS

def plot_rel_pos(rel_position):
    '''
    Takes relative positions from interatomic_distance[1] function
    Creates x y z lits of coordinates to be plotted
    '''
    x_position = [0]
    y_position = [0]
    z_position = [0]

    for i, coords in enumerate(rel_position):
            x_position.append(rel_position[i][0])
            y_position.append(rel_position[i][1])
            z_position.append(rel_position[i][2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_position, y_position, z_position, c='r', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

## Plot data
    plt.show()

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                     AVERAGE SUPERCELL "GRID"

def average_grid(orthonormal_positions, av_cell_param):
    orthonormal_positions = orthonormalise(cell, atom_list)
    

###
###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###---------------------------------------------------------------------
###                         WRITE OUT FILES

def writeout(data):
    '''
    Writes out data to *.csv file in /write_out directory
    '''
    
    write_out_path = cwd + '/write_out/'
    pass

###
###---------------------------------------------------------------------
###=====================================================================
