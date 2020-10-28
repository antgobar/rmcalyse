### --------------------------------------------------------------------
###
### Supercell class
###
###
### --------------------------------------------------------------------
import re
import numpy as np

example_path = '/Users/Anton/Documents/Python_Programs/rmcalyse/rmcalyse/read_in/STO_2.rmc6f'


class SuperCell():

    def __init__(self, file_path):

        self.file_path = file_path
        self.cell_parameters = None
        self.elements = None
        self.atom_list = None
        self.supercell_size = None
        self.density = None
        self.volume = None
        self.orth_pos = None
        self.orth_lbl_pos = None
        

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
            # Atom list
            if line.find('[1]') >= 0:
                atom_list_lines.append(line)

        # Put element, atom no. and atomic positions etc. into lists

        # Elements
        key = 'Atom types present:'
        lead_str, keyword, elements_str = line_elements.partition(key)
        elements_str = elements_str.strip()
        elements = re.sub("[^\w]", " ", elements_str).split()

        # Density - currently not used
        temp = re.findall('\d+\.\d+', line_density)
        density = [float(i) for i in temp]

        # supercell dimensions - currently not used
        temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell_size)
        supercell_size = [int(i) for i in temp]

        # supercell parameters: a, b, c, alpha, beta, gamma
        temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
        cell_parameters = [float(i) for i in temp]

        # Create atom list of lists, format:
        # [element, number, position x, position y, position z]
        atom_list = []
        for line in atom_list_lines:
            temp_list = []
            split = line.split()
            element = split[1]
            number = int(split[0])
            pos_x = float(split[3])
            pos_y = float(split[4])
            pos_z = float(split[5])
            temp_list.append(element)
            temp_list.append(number)
            temp_list.append(pos_x)
            temp_list.append(pos_y)
            temp_list.append(pos_z)
            atom_list.append(temp_list)

        self.cell_parameters = cell_parameters
        self.elements = elements
        self.atom_list = atom_list
        self.supercell_size = supercell_size
        self.density = density


    def volume_matrix(self):
        """Converion to orthonormal atomic positions"""
        # Initialise matrix 
        cell = self.cell_parameters
        atom_list = self.atom_list
        
        a = self.cell_parameters[0]
        b = self.cell_parameters[1]
        c = self.cell_parameters[2]

        al = np.deg2rad(self.cell_parameters[3])
        be = np.deg2rad(self.cell_parameters[4])
        ga = np.deg2rad(self.cell_parameters[5])

        volume = a*b*c * (1 - np.cos(al)**2 - np.cos(be)**2 - \
        np.cos(ga)**2 + 2*np.cos(al)*np.cos(be)*np.cos(ga))**0.5

        a1 = a
        a2 = 0
        a3 = 0

        b1 = b * np.cos(ga)
        b2 = b * np.sin(ga)
        b3 = 0

        c1 = c * np.cos(be)
        c2 = c * (np.cos(al) - (np.cos(be) * \
             np.cos(ga))) / np.sin(ga)
        c3 = volume / (a * b * np.sin(ga))

        M = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])


        ## returns
        # Supercell volume
        self.supercell_volume = volume
        # Volume of a single cell (average)
        self.average_cell_volume = volume / np.prod(self.supercell_size)
        # Transformation matrix
        self.matrix = M
        
        
        # Orthonormalisation a set of coordinates using with
        # the transformation matrix M (self.matrix).
    def orthonormalise_cell(self):

        M = self.matrix
        
        labels = np.array(self.atom_list[:,:2])
        atomic_positions = np.array(self.atom_list[:,2:5])
        atomic_positions = 
        orthonormal_positions = (M @ atom_positions.transpose()).transpose()

        self.orth_pos = orthonormal_positions

        # join labels and positions
        orthornormal_labels_positions = np.hstack((labels, orth_pos))

        self.orth_lbl_pos = orthornormal_labels_positions
        
        

        
            

        
            
        


