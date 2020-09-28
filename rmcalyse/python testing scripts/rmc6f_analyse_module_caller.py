###========================================================================
###------------------------------------------------------------------------
###
###     RMCAlyse apha by A.G.B & W.S. - Master file
###
###     Modules:
###
###     read_rmc6f
###     orthonormalise
###     interatomic_distance
###     average_cell
###
###------------------------------------------------------------------------
###========================================================================

import time
import read_rmc6f as r_r
import orthonormalise as o_n
import interatomic_distance as i_d
import average_cell as a_c

start_time = time.time()

file_in = 'SrTiO3_00Nb_222.rmc6f'

cell = r_r.read_in(file_in)[0]
atom_list = r_r.read_in(file_in)[1]
##elements = r_r.read_in('SrTiO3_00Nb_222.rmc6f')[2]

orthonormal_positions = o_n.orthonormalise(cell, atom_list)

i_a_dist_list = i_d.interatomic_distance(orthonormal_positions,\
                                         ['Bi', 'Pb'], 'Ti', 4, 1)[0]

##rel_dist = i_d.interatomic_distance(orthonormal_positions, \
##                                    'Bi', 'Ti', 4, 1)[1]
##
average_cell_parameter = a_c.average_cell(orthonormal_positions, 'Ti')

time_taken = time.time() - start_time
print('\nTotal time taken: ', round(time_taken, 3), ' seconds.', '\n')
