###------------------------------------------------------------------------
###
### Program/module to calculate average cell parameter 
### 
### Requires interatomic_distance module
###
### Example of how to call this module
###
### import average_cell as a_c
###
### average_cell_parameter = \
### a_c.average_cell(interatomic_distance_list, 'Ti')
###
###------------------------------------------------------------------------

# Interatomic distances called from interatomic_distance module
import numpy as np
import interatomic_distance as i_d

# cell_param_list of atom atom distances
def average_cell(orthonormal_positions, atom):

    cell_param_list = interatomic_distance(orthonormal_positions,\
                                               atom, atom, 4.5, 1)[0]
    # Cell parameters to be averaged
    to_ave = []
    
    for dist, i in enumerate(cell_param_list):
            val = cell_param_list[dist][4]
            to_ave.append(val)
        
    av_cell_param = np.around(np.average(to_ave), 3)

    return(av_cell_param)
