### Main File ###

# core imports
from core import rmcalyse_welcome
from core import read_rmc6f
from core import orthonormalise
from core.supercell_class import SuperCell

# plugin imports
from plugins.centroid_vector import centroid_vector

file_path = 'read_in/SrTiO3_00Nb.rmc6f'

# create rmc object
rmc_data = SuperCell(file_path)

# fetch data from rmc6f file
rmc_data.get_data()

# orthonormalise cell
rmc_data.orthonormalise_cell()

atomA = ['Ti']
atomB = ['Sr']
max_d = 4  # max distance for centroid polyhedra
coordinatin_no = 8  # Coordination number for centroid calc

centroid_vector, centroid_position = centroid_vector.get_centroids(
    orthonormal_positions,
    atomA,
    atomB,
    max_d,
    coordinatin_no
    )




