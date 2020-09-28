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
### C.  Calculate interatomic distances
###
### D.  Plot collapsed cell centered on an atom
###
###------------------------------------------------------------------------
###========================================================================

###------------------------------------------------------------------------
### A. GET DATA FROM FILE
###------------------------------------------------------------------------

### QUICK CONTROLS
writeout = False

# Import desired libraries
import os
import numpy as np
import re                   # look through text file for relevant data
import time
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Time whole process
start_time = time.time()

cwd = os.getcwd()

# Open *.rmc6f file (remember to set appropriate working directory!)
read_in_path = cwd + '/read_in/'
write_out_path = cwd + '/write_out/'

file_in = 'NBT-PT08.rmc6f'

rmc6f_input = open(read_in_path + file_in, 'r')

line_density = []
line_supercell = []
line_cell =[]
line_atom_list = []

print('\nReading file:', file_in, '...')

# Extract and save variables 
for line in rmc6f_input:
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
print('\nFile is closed: ', rmc6f_input.closed)

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

atom_list_head = ['Atom', 'no.', 'x.', 'y', 'z']
print('\nFormat of atom list: ', atom_list_head, atom_list[0], sep = '\n')

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

# Orthonormal real position function
def ortho_position(atom):
    orth_pos = np.around(((M @ atom.transpose()).transpose()), 3)
    list_pos = np.array(orth_pos).ravel().tolist()
    return(list_pos)

# Initialise ortho position list
orthonormal_positions = []

# Iterate over atoms and calculate orthonormal positions
for n, atom in enumerate(atom_list):
    atom = np.array([atom_list[n][2:5]])
    label = atom_list[n][:2]
    atomI = ortho_position(atom)
    orthonormal_positions.append(label + atomI)

print('\nFormat of atom orthonormalised list \
(coordinates are REAL, not fractional): ', atom_list_head,\
      orthonormal_positions[0], sep = '\n')

# Write orthonormal positions to .csv file
file_out = file_in[:-6] + '_ortho_pos.csv'

if writeout == True:
    with open(write_out_path + file_out, 'w', newline = '') as f:
        writer = csv.writer(f)
        for i in orthonormal_positions:
            writer.writerow([i])
else:
    pass

###------------------------------------------------------------------------
### C. CALCULATE INTERATOMIC DISTANCES
###------------------------------------------------------------------------

def interatomic_distance(atomA, atomB):
    int_dist = np.around((sum((np.array(atomA)-np.array(atomB))**2)**0.5),3)
    return(int_dist)

interatomic_distance_list = []
relative_position = []

# Iterate over atoms and calculate distances
for nA, atom in enumerate(orthonormal_positions):
    # Pick 1st atom - Loop and then pick 2nd etx
    atomA = orthonormal_positions[nA][2:5]
    labelA = orthonormal_positions[nA][:2]
    for nB, atom in enumerate(orthonormal_positions):
        # Distance of 1st atoms to all atoms
        atomB = orthonormal_positions[nB][2:5]
        labelB = orthonormal_positions[nB][:2]
        distance = interatomic_distance(atomA, atomB)


        if distance <= 2.5 \
        and distance >= 0 \
        and orthonormal_positions[nA][0] == 'Ti' \
        and orthonormal_positions[nB][0] == 'O':
        # Make sure you're selecting the correct atoms edit as needed
            # Interatomic distance for selected atoms
            interatomic_distance_list.append(labelA + labelB + [distance])
            # relative position (for cell collapse function)
            relative_position.append(np.array(atomA) - np.array(atomB))

header = ['atom A', 'A no.', 'B no.', 'Distance (A)']
labeled_d = [header] + interatomic_distance_list
print('\nFormat of interatomic distances: ', labeled_d[0], labeled_d[1], sep = '\n')

# Write distances to .csv file
file_out = file_in[:-6] + '_orth_dist.csv'


if writeout == True:
    with open(write_out_path + file_out, 'w', newline = '') as f:
        writer = csv.writer(f)
        for i in labeled_d:
            writer.writerow([i])

else:
    pass


###------------------------------------------------------------------------
### D. PLOT COLLAPSED UNIT CELL - CENTERED ON ATOM X
###------------------------------------------------------------------------

x_position = [0]
y_position = [0]
z_position = [0]


for i, coords in enumerate(relative_position):
        x_position.append(relative_position[i][0])
        y_position.append(relative_position[i][1])
        z_position.append(relative_position[i][2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_position, y_position, z_position, c='r', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Plot data
plt.show()

###------------------------------------------------------------------------
### E. AVERAGE CELL PARAMETER
###------------------------------------------------------------------------

cell_param = []

for dist, i in enumerate(interatomic_distance_list):
	val = interatomic_distance_list[dist][4]
	to_ave.append(val)
    
av_cell_param = np.average(to_ave)


def average_cell(cell_param_list, atom):

    cell_param_list = interatomic_distance(orthonormal_positions, atom, atom, 4.5, 1)[0]

    # Cell parameters to be averaged
    to_ave = []
    
    for dist, i in enumerate(cell_param_list):
            val = cell_param_list[dist][4]
            to_ave.append(val)
        
    av_cell_param = np.around(np.average(to_ave), 3)

    return(av_cell_param)


###========================================================================
# Total time taken for program to execute and write files

print('\nWrite output files?: ', writeout)

time_taken = time.time() - start_time

print('\nTotal time taken: ', round(time_taken, 3), ' seconds.', '\n')


###========================================================================




###========================================================================
###------------------------------------------------------------------------
###
###     THANK YOU FOR PARTICIPATING
###
###     CHECK YOUR FOLDER FOR OUTPUT FILES
###
###------------------------------------------------------------------------
###========================================================================
