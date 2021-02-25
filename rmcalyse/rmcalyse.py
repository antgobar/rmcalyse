### Main File ###
import numpy as np
import pandas as pd
# core imports
from core import rmcalyse_welcome
from core.supercell_class import SuperCell

# plugin imports
from plugins.distance_calculations.distance_class import Distance
from plugins.centroid_vector.centroid_class import Centroid

import time

file_path = 'read_in/SrTiO3_30Nb_SCARF.rmc6f'

# create rmc object
rmc_data = SuperCell(file_path)

# fetch data from rmc6f file
rmc_data.get_data()
df = pd.DataFrame.from_records(rmc_data.atom_list, columns=rmc_data.position_list_header)
rmc_data.orthonormalise_cell()


rmc_centroid = Centroid(rmc_data.position_labels, rmc_data.raw_basis_positions)
rmc_centroid.get_centroid_vectors('Sr','Ti', 8, rmc_data.matrix)

print(len(rmc_centroid.non_zero_vectors))
print(rmc_centroid.non_zero_vectors[:, 0])
