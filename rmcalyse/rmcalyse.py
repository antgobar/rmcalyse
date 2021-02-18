### Main File ###
import numpy as np
# core imports
from core import rmcalyse_welcome
from core import read_rmc6f
from core import orthonormalise
from core.supercell_class import SuperCell

# plugin imports
from plugins.centroid_vector import centroid_vector


file_path = 'read_in/STO_1.rmc6f'

# create rmc object
rmc_data = SuperCell(file_path)

# fetch data from rmc6f file
rmc_data.get_data()

# orthonormalise cell
rmc_data.orthonormalise_cell()

orth_labels = rmc_data.orth_labels
orthonormal_positions = rmc_data.orthonormal_positions

atomA = ['Ti']
atomB = ['Sr']
max_d = 4  # max distance for centroid polyhedra
coordination_no = 8  # Coordination number for centroid calc


print(orthonormal_positions)

