### Main File ###

# core imports
from core import rmcalyse_welcome
from core import read_rmc6f
from core import orthonormalise
from core.supercell_class import SuperCell

# plugin imports
from plugins.centroid_vector import centroid_vector

file_path = 'read_in/SrTiO3_00Nb.rmc6f'
##rmc6f_data = read_rmc6f.read_in(file_in)
##
##cell, atom_list, elements = rmc6f_data
##orthonormal_positions = orthonormalise.orthonormalise(cell, atom_list)
##
##atomA = ['Ti']
##atomB = ['Sr']
##
##centroid_shell_d = 4  # max distance for centroid polyhedra
##coord_no = 8  # Coordination number for centroid calc
##
##centroid_vector, centroid_position = centroid_vector.get_centroids(
##    orthonormal_positions,
##    atomA,
##    atomB,
##    centroid_shell_d,
##    coord_no
##    )




