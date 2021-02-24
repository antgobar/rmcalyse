# --------------------------------------------------------------------
###
# Supercell class:
# Methods
# get_data(): reads in rmc6f file from the set file path
# orthonormalise_cell(): converts atomic coordinates to an orthonormal basis
###
# --------------------------------------------------------------------

import re
import numpy as np
import pandas as pd

class SuperCell():

    def __init__(self, file_path):

        self.file_path = file_path
        

    def get_data(self):

        with open(self.file_path, 'r') as f:
            rmc_data = f.readlines()

        atom_list_lines = []

        # Loop through file to find matching strings
        for line in rmc_data:
            # Elements
            if line.find('Atom types present:') >= 0:
                line_elements = line
            # Number densty
            if line.find('Number density') >= 0:
                line_density = line
            # Supercell dimensions
            if line.find('Supercell') >= 0:
                line_supercell_size = line
            # Supercell parameters
            if line.find('Cell') >= 0:
                line_cell = line
            # Atom list ### TESTS NEEDED
            if line.find('[') >= 0:
                atom_list_lines.append(line)

        # Put element, atom no. and atomic positions etc. into lists
        
        # Elements
        key = 'Atom types present:'
        lead_str, keyword, elements_str = line_elements.partition(key)
        elements_str = elements_str.strip()
        elements = re.sub("[^\w]", " ", elements_str).split()

        # Density
        temp = re.findall('\d+\.\d+', line_density)
        density = [float(i) for i in temp]

        # supercell dimensions
        temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell_size)
        supercell_size = [int(i) for i in temp]

        # supercell parameters: a, b, c, alpha, beta, gamma
        temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
        cell_parameters = [float(i) for i in temp]

        # Create atom list array, format:
        # [element, number, position x, position y, position z]

        df = pd.DataFrame(atom_list_lines)
        atom_list = np.array(df.iloc[:,0].str.split().tolist())

        # create atributes
        self.atom_list = atom_list
        self.cell_parameters = cell_parameters
        self.elements = elements
        self.supercell_size = supercell_size
        self.density = density  

        self.position_list_header = ['ID', 'Element', 'mult', 'x', 'y', 'z', 'subcell', 'h','k','l']
        self.position_labels = self.atom_list[:, :2]      


    def orthonormalise_cell(self):
        """
        Orthonormalisation of a set of 3D coordinates.
        Coordinates taken from <atom_list>
        Original basis taken grom <cell_parameters>
        """
        #--------------------------------------------------------------#
        # Initialise transformation matrix M
        #--------------------------------------------------------------#

        a, b, c, al, be, ga = self.cell_parameters

        al = np.deg2rad(al)
        be = np.deg2rad(be)
        ga = np.deg2rad(ga)
        
        volume = (a * b * c *
                  (1 - np.cos(al)**2
                   - np.cos(be)**2
                   - np.cos(ga)**2
                   + 2 * np.cos(al)
                   * np.cos(be)
                   * np.cos(ga))
                  ** 0.5)
        
        a1 = a
        a2 = 0
        a3 = 0

        b1 = b * np.cos(ga)
        b2 = b * np.sin(ga)
        b3 = 0

        c1 = c * np.cos(be)
        c2 = c * (np.cos(al) - (np.cos(be) *
                                np.cos(ga))) / np.sin(ga)
        c3 = volume / (a * b * np.sin(ga))

        M = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])

        self.supercell_volume = volume

        self.average_cell_volume = volume / np.prod(self.supercell_size)

        self.matrix = M
        
        # x, y, z raw basis positions
        raw_basis_positions = self.atom_list[:, 3:6]

        #--------------------------------------------------------------#
        # Orthonormalisation calculaion
        #--------------------------------------------------------------#

        # Make dtype float64
        self.raw_basis_positions = np.float64(raw_basis_positions)

        # Orthonormalisation of atomic positions
        orthonormal_positions = np.dot(M, self.raw_basis_positions.T).T

        # Round to make very small values (e.g. ~10e-16), zero.
        # parse orthonormal positions to class instance
        self.orthonormal_positions = np.around(orthonormal_positions, 8)

        #--------------------------------------------------------------#

        def make_df(self, positions):
            df = pd.DataFrame.from_records(positions, columns=self.position_list_header)
            self.positions_df = df
