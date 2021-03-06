
###------------------------------------------------------------------------
###
### Program/module to read *.rmc6f file and get data
### e.g. cell dimension and atomic positions
###
### Example of how to call this module:
###
### import read_rmc6f as rr
###
### cell = rr.read_in('SrTiO3_00Nb_222.rmc6f')[0]
### atom_list = read_in('SrTiO3_00Nb_222.rmc6f')[1]
###
###------------------------------------------------------------------------

import os
import re           # look through text file for relevant data


# Open *.rmc6f file 
cwd = os.getcwd()
read_in_path = cwd + '/read_in/'
write_out_path = cwd + '/write_out/'

def read_in(file_in):

    rmc6f_input = open(read_in_path + file_in, 'r')

    line_elements = []
    line_density = []
    line_supercell = []
    line_cell =[]
    line_atom_list = []

##    print('\nReading file:', file_in, '...')

    # Extract and save variables
    for line in rmc6f_input:
            #	header
            if line.find('Atom types present:') >= 0:
                line_elements = line
            if line.find('Number density') >= 0:
                line_density = line
            if line.find('Supercell') >= 0:
                line_supercell = line
            if line.find('Cell') >= 0:
                line_cell = line
            #	atom lines
            if line.find('[1]') >= 0:
                    line_atom_list.append(line)


    # Close file!
    rmc6f_input.close()
##    print('\nFile is closed: ', rmc6f_input.closed)

    # Put element, atom no. and atomic positions into lists
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_elements)   ### FIX
    elements = [float(i) for i in temp]                     ### FIX
    temp = re.findall('\d+\.\d+', line_density)
    density = [float(i) for i in temp]
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell)
    supercell = [int(i) for i in temp]
    temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
    cell = [float(i) for i in temp] # Need this for interatomic distances

    atom_list = []
    for line in line_atom_list:
            temp = []
            temp_1 = re.findall(r'\b\d+\b', line)       #	ints
            temp_2 = re.findall('[a-zA-Z]+', line)  	#	letters
            temp_3 = re.findall('\d+\.\d+', line)   	#	floats
            temp.append(temp_2[0])
            temp.append(int(temp_1[0]))
            temp.append(float(temp_3[0]))
            temp.append(float(temp_3[1]))
            temp.append(float(temp_3[2]))
            atom_list.append(temp)

    atom_list_head = ['Atom', 'no.', 'x.', 'y', 'z']
##    print('\nFormat of atom list (non orthonormalised): ',\
##        atom_list_head, atom_list[0], sep = '\n')

    return(cell, atom_list, elements, supercell, density)
    
