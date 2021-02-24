### Main File ###
import numpy as np
import pandas as pd
# core imports
from core import rmcalyse_welcome
from core.supercell_class import SuperCell

# plugin imports
from plugins.distance_calculations.distance_class import Distance

import time

file_path = 'read_in/SrTiO3_00Nb.rmc6f'

# create rmc object
rmc_data = SuperCell(file_path)

# fetch data from rmc6f file
rmc_data.get_data()
df = pd.DataFrame.from_records(rmc_data.atom_list, columns=rmc_data.position_list_header)


# orthonormalise cell
rmc_data.orthonormalise_cell()

# distances
rmc_distances = Distance(rmc_data.position_labels, rmc_data.raw_basis_positions)
rmc_distances.array_distance_orthonormaliser('Sr', 'Ti', rmc_data.matrix)
rmc_distances.make_distance_labels()
rmc_distances.make_df()
rmc_distances.distance_window_filter(1, 4)

print(rmc_distances.distance_df)



