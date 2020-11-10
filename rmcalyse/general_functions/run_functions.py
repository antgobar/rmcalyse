# file to test functions

from supercell_class import *
import numpy as np

import interatomic_distance as iad

example_path = '/Users/Anton/Documents/Python_Programs/rmcalyse/rmcalyse/read_in/STO_2.rmc6f'

rmc_example = SuperCell(example_path)
rmc_example.get_data()
rmc_example.orthonormalise_cell()

op = rmc_example.orth_positions
