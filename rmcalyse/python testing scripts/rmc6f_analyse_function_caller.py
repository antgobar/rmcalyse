###=====================================================================
###---------------------------------------------------------------------
###
###     RMCAlyse apha by A.G.B & W.S. - Function caller
###
###     Calls rmc6f_analyse_functions.py 
###
###---------------------------------------------------------------------
###=====================================================================

import rmc6f_analyse_functions as raf ## FUNCTIONS FILE
import time

start_time = time.time()

###=====================================================================
###---------------------------------------------------------------------
## USER INPUTS
## *rmc6f file to read,
## atomA or center atom for centroid function
## atomB or orbit atom for centroid function
## Can input list of atoms e.g. "atomB = ['Zr', 'Ti']" in PZT
## max search distance, min search distance,
## coordination number for atom pair
## Averace cell parameter calculated from one atom type

file_in = 'STO_10.rmc6f'
atomA, atomB = 'Ti', 'O'
max_d, min_d = 3, 1
coord_no = 6
param_atom = 'Sr'
max_param = 4.5
hist_bin_w = 0.01

## CONTROL STATION

###---------------------------------------------------------------------
###=====================================================================

## Read function
cell = raf.read_in(file_in)[0]
atom_list = raf.read_in(file_in)[1]
##elements = r_r.read_in('SrTiO3_00Nb_222.rmc6f')[2]

#### Orthonormalisation function
##orthonormal_positions = raf.orthonormalise(cell, atom_list)

#### Interatomic distance function
##i_a_dist_list = raf.interatomic_distance(orthonormal_positions, atomA, atomB, max_d, min_d)[0]

#### Centroid function
##centroid_vector = raf.centroid(orthonormal_positions, atomA, atomB, max_d, coord_no)[0]                             

#### Average cell parameter calculated. 
##av_cell_param = raf.av_unit_cell(orthonormal_positions, param_atom, max_param)
##print('\nAverage unit cell parameter (A)', av_cell_param, sep = '\n')

#### Relative position function
##rel_position = raf.interatomic_distance(orthonormal_positions, atomA, atomB, max_d, min_d)[1]
##
#### Plot relative positions centred on atomA
##raf.plot_rel_pos(rel_position)

#### IAD histogram plotter
##raf.iad_hist(i_a_dist_list, atomA, atomB, min_d, max_d, hist_bin_w)

## print examples of output formats

#### Use average cell parameter to ... not really useful at the moment..
##fractional_coordinates = raf.frac_coord(orthonormal_positions, av_cell_param)

## Total time for all functions called
total_time = time.time() - start_time
print('\nTotal time taken: ', round(total_time, 3), ' seconds.', '\n')
