import numpy as np

class distance():

    def __init__(self, cell_parameters, atomic_positions, basis=False):
        self.positions = atomic_positions
        self.basis = None
