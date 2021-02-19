### Main File ###
import numpy as np
# core imports
from core import rmcalyse_welcome
from core import read_rmc6f
from core import orthonormalise
from core.supercell_class import SuperCell

# plugin imports
from plugins.centroid_vector import centroid_vector

import time

file_path = 'read_in/STO_10.rmc6f'

# create rmc object
rmc_data = SuperCell(file_path)

# fetch data from rmc6f file
rmc_data.get_data()

print(rmc_data.atom_list[:5])

# orthonormalise cell
rmc_data.orthonormalise_cell()

atom_positions = rmc_data.raw_basis_positions
position_labels = rmc_data.position_labels
orthonormal_positions = rmc_data.orthonormal_positions


# atomA = ['Ti']
# atomB = ['Sr']
# max_d = 4  # max distance for centroid polyhedra
# coordination_no = 8  # Coordination number for centroid calc

# matrix = rmc_data.matrix