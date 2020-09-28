###========================================================================
###------------------------------------------------------------------------
###
###     RMCAlyse apha by A.G.B & W.S.
###
### A.  Program to read *.rmc6f file and get data
###     e.g. cell dimension and atomic positions
###
### B.  Then calculate interatomic positions form a non-orthonormal basis
###
###     May need prettfying and functionifying at some point
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

start_time = time.time()

# Open *.rmc6f file (remember to set appropriate working directory!)
file_in = 'SrTiO3_00Nb_222.rmc6f'

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
### B. CALCULATE INTERATOMIC DISTANCES
###------------------------------------------------------------------------

# Lattice parameters - unit cell length and angles
a = cell[0]
b = cell[1]
c = cell[2]

al = np.deg2rad(cell[3])
be = np.deg2rad(cell[4])
ga = np.deg2rad(cell[5])

# Triclinic (universal) Metric Tensor
g=np.array([[a ** 2, a * b * np.cos(ga), a * c * np.cos(be)], \
[b * a * np.cos(ga),b ** 2 , b * c * np.cos(al)], \
[c * a * np.cos(be), c * b * np.cos(al), c ** 2]])

# Interatomic distance function
def interatomic_distance(atomA, atomB):
    vBA = atomB - atomA # Net vector
    dBA = (vBA @ g @ vBA.transpose()) ** 0.5 # Orthonormal distance between A and B
    return(dBA)

# Initialise distance list

labeled_dist = []

# Iterate over atoms and calculate distances
for nA, atom in enumerate(atom_list): # Pick 1st atom - Loop and then pick 2nd etx
    atomA = np.array([atom_list[nA][2:5]])
    labelA = atom_list[nA][:2]
    
    for nB, atom in enumerate(atom_list): # Distance of 1st atoms to all atoms
        atomB = np.array([atom_list[nB][2:5]])
        labelB = atom_list[nB][:2]
        dist = interatomic_distance(atomA, atomB)
        if dist < 5 and atom_list[nA][0] == 'Ti':
        # Make sure you're selecting the correct atom!
            dist_list = float(str(np.around(dist, 3)).replace('[','').replace(']',''))
            # remove brackets?
            labeled_dist.append(labelA + labelB + [dist_list])

header = ['atom A', 'A no.', 'B no.', 'Distance (A)']

labeled_d = [header] + labeled_dist

print('\nFormat of interatomic distances: ', labeled_d[0], labeled_d[1], sep = '\n')

# Write distances to .csv file

file_out = file_in[:-6] + '_distance_list.csv'

with open(file_out, 'w', newline = '') as f:
    writer = csv.writer(f)
    for i in labeled_dist:
        writer.writerow([i])

end_time = time.time()

time_taken = end_time - start_time

print('\nTotal time taken: ', round(time_taken, 3), ' seconds.')
