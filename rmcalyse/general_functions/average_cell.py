import numpy as np

from general_functions import interatomic_distance as iad


def av_unit_cell(orthonormal_positions, atom, max_param):
    '''
    Takes in list of atomic coordinates in orthonormal basis.
    Returns average of nearest neighbour distances for specified atom.
    This average can be considered the average unit cell parameter
    '''

    cell_param_list = iad.interatomic_distance(orthonormal_positions,
                                               atom, atom, 1, max_param)[0]
    # Cell parameters to be averaged
    to_ave = []

    for dist, i in enumerate(cell_param_list):
        val = cell_param_list[dist][10]
        to_ave.append(val)

    av_cell_param = np.around(np.average(to_ave), 4)

    return(av_cell_param)
