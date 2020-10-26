# ------------------------------------------------------------------------
###
# Supercell class
###
###
# ------------------------------------------------------------------------
import re
class SuperCell():

    def __init__(self, file_path):
        self.file_path = file_path
        self.cell_parameters = None
        self.elements = None
        self.atom_list = None
        self.supercell_size = None
        self.density = None

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

        # Put element, atom no. and atomic positions into lists

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


path2 = '/Users/Anton/Documents/Python_Programs/rmcalyse/rmcalyse/read_in/STO_2.rmc6f'
