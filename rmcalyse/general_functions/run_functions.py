# file to test functions

from supercell_class import *
from vectorised_iad import iad_mt
import numpy as np

example_path = '/Users/Anton/Documents/Python_Programs/rmcalyse/rmcalyse/read_in/STO_2.rmc6f'

rmc_example = SuperCell(example_path)
rmc_example.get_data()
rmc_example.orthonormalise_cell()

orthonormal_positions = rmc_example.orth_pos
cell = rmc_example.cell_parameters

