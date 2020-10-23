###------------------------------------------------------------------------
###
### Supercell class
###
###
###------------------------------------------------------------------------
import re
class SuperCell():
    
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self):
        rmc6f_data =  open(self.file_path, 'r')

        line_elements = []
        line_density = []
        line_supercell = []
        line_cell = []
        line_atom_list = []

        # Loop through file to find matchin strings
        for line in rmc6f_data:
            # Elements
            if line.find('Atom types present:') >= 0:
                line_elements = line
            # Number densty
            if line.find('Number density') >= 0:
                line_density = line
            # Supercell dimensions
            if line.find('Supercell') >= 0:
                line_supercell = line
            # Supercell parameters 
            if line.find('Cell') >= 0:
                line_cell = line
            # Atom list
            if line.find('[1]') >= 0:
                line_atom_list.append(line)

        rmc6f_data.close()

        # Put element, atom no. and atomic positions into lists
        # Elements
        key = 'Atom types present:'
        lead_str, keyword, elements_str = line_elements.partition(key)
        elements_str= elements_str.strip()
        elements = re.sub("[^\w]", " ",  elements_str).split()

        # Density - currently not used
        temp = re.findall('\d+\.\d+', line_density)
        density = [float(i) for i in temp]        

        # supercell dimensions - currently not used
        temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell)
        supercell = [int(i) for i in temp]

        # supercell parameters: a, b, c, alpha, beta, gamma
        temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
        cell_parameters = [float(i) for i in temp]

        atom_list = []
        for line in line_atom_list:
            temp = []
            temp_1 = re.findall(r'\b\d+\b', line)  # ints
            temp_2 = re.findall('[a-zA-Z]+', line)  # letters
            temp_3 = re.findall('\d+\.\d+', line)  # floats
            temp.append(temp_2[0])
            temp.append(int(temp_1[0]))
            temp.append(float(temp_3[0]))
            temp.append(float(temp_3[1]))
            temp.append(float(temp_3[2]))
            atom_list.append(temp)

               
        return cell_parameters, atom_list, elements

    def cell_parameters(self):
        return self.get_data()[0]

    def elements(self):
        return self.get_data()[3]

    def elements(self):
        return self.get_data()[3]

    
path2 = '/Users/Anton/Documents/Python_Programs/rmcalyse/rmcalyse/read_in/STO_2.rmc6f'

