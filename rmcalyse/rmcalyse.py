### Main File ###
import numpy as np

# core imports
from core import rmcalyse_welcome
from core.supercell_class import SuperCell

# plugin imports
from plugins.distance_calculations.distance_class import Distance

import time

file_path = 'read_in/STO_2.rmc6f'

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

# distances
rmc_distances = Distance(position_labels, atom_positions)
rmc_distances.array_distance_orthonormaliser('Sr', 'Ti', rmc_data.matrix)

print(rmc_distances.distances_list.flatten())