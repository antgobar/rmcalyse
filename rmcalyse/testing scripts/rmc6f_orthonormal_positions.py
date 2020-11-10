###========================================================================
###------------------------------------------------------------------------
###
###     RMCAlyse apha by A.G.B & W.S.
###
### A.  Program to read *.rmc6f file and get data
###     e.g. cell dimension and atomic positions
###
### B.  Convert atomic positions to orthonormal coordinates
###
### C.  Calculate interatomic positions
###
###------------------------------------------------------------------------
###========================================================================


###------------------------------------------------------------------------
### A. GET DATA FROM FILE
###------------------------------------------------------------------------

# Import desired libraries
import os
import numpy as np         
import re                   # look through text file for relevant data
import time
import csv

# Time whole process
start_time = time.time()



# Open *.rmc6f file (remember to set appropriate working directory!)
file_in = 'NBT-PT08.rmc6f'

rmc6f_input = open(file_in, 'r')

line_density = []
line_supercell = []
line_cell =[]
line_atom_list = []

# Extract and save structure parameters
for line in rmc6f_input:
	#	header
	if line.find("Number density") >= 0:
		line_density = line
	if line.find("Supercell") >= 0:
		line_supercell = line
	if line.find("Cell") >= 0:
		line_cell = line
	#	atom lines
	if line.find("[1]") >= 0:
		line_atom_list.append(line)		

# Close file!
rmc6f_input.close()
print("\nFile is closed: ", rmc6f_input.closed)

# Put element, atom no. and atomic positions into lists
temp = re.findall('\d+\.\d+', line_density)
density = [float(i) for i in temp]
temp = re.findall('[-+]?\d*\.\d+|\d+', line_supercell)
supercell = [int(i) for i in temp] 
temp = re.findall('[-+]?\d*\.\d+|\d+', line_cell)
cell = [float(i) for i in temp] # Need this for interatomic distances

atom_list = []
for line in line_atom_list:
	temp = []
	temp_1 = re.findall(r'\b\d+\b', line)		#	ints
	temp_2 = re.findall('[a-zA-Z]+', line)		#	letters
	temp_3 = re.findall('\d+\.\d+', line)		#	floats
	temp.append(temp_2[0])
	temp.append(int(temp_1[0]))
	temp.append(float(temp_3[0]))
	temp.append(float(temp_3[1]))
	temp.append(float(temp_3[2]))
	atom_list.append(temp)

a_list_head = ['Atom', 'no.', 'x.', 'y', 'z']
print('\nFormat of atom list: ', a_list_head, atom_list[0], sep = '\n')

###------------------------------------------------------------------------
### B. CONVERT TO ORHTONORMAL COORDINATES
###------------------------------------------------------------------------

# Lattice parameters - unit cell length and angles
a = cell[0]
b = cell[1]
c = cell[2]

al = np.deg2rad(cell[3])
be = np.deg2rad(cell[4])
ga = np.deg2rad(cell[5])

V = a*b*c * (1 - np.cos(al)**2 - np.cos(be)**2 - \
np.cos(ga)**2 + 2*np.cos(al)*np.cos(be)*np.cos(ga))**0.5

#Converion to orthonormal
a1 = a
a2 = 0
a3 = 0

b1 = b * np.cos(ga)
b2 = b * np.sin(ga)
b3 = 0

c1 = c * np.cos(be)
c2 = c * (np.cos(al) - (np.cos(be) * np.cos(ga))) / np.sin(ga)
c3 = V / (a * b * np.sin(ga))

M = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])

# Interatomic distance function
def ortho_position(atom):
    orth_pos = (M @ atom.transpose()).transpose()
    list_pos = np.array(orth_pos).ravel().tolist()
    return(list_pos)

# Initialise ortho position list

labeled_positions = []

# Iterate over atoms and calculate orthonormal positions
for n, atom in enumerate(atom_list): 
    atom = np.array([atom_list[n][2:5]])
    label = atom_list[n][:2]
    atomX = ortho_position(atom)
    labeled_positions.append(label + atomX)

print('\nFormat of atom orthonormalised list: ', a_list_head,\
      labeled_positions[0], sep = '\n')


# Write orthonormal positions to .csv file
file_out = file_in[:-6] + '_ortho_pos.csv'

with open(file_out, 'w', newline = '') as f:
    writer = csv.writer(f)
    for i in labeled_positions:
        writer.writerow([i])

end_time = time.time()

time_taken = end_time - start_time

print('\nTotal time taken: ', round(time_taken, 3), ' seconds.')
