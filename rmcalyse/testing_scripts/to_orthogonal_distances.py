###------------------------------------------------------------------------
###
### Program to copute interatomic distances from a non-orthonomal basis
###
###------------------------------------------------------------------------

# Import relevant libraries

import numpy as np
import os


# Lattice parameters - unit cell length and angles
a = 1
b = 1
c = 1

al = np.deg2rad(90)
be = np.deg2rad(90)
ga = np.deg2rad(90)


# Atomic positions
atomA = np.array([[0, 0, 0]]) # [0, 0, 0] for vector origin
atomB = np.array([[0, 0, 1]]) # position of iterest (fractional)
atomC = np.array([[0, 1, 0]]) # 2nd position of interest (mainly for angle calcs)

# Vector or  positions relative to atomA 

vBA = atomB - atomA
vCA = atomC - atomA
vBC = atomB - atomC

# Triclinic Metric Tensor
g=np.array([[a ** 2, a * b * np.cos(ga), a * c * np.cos(be)], \
[b * a * np.cos(ga),b ** 2 , b * c * np.cos(al)], \
[c * a * np.cos(be), c * b * np.cos(al), c ** 2]])

# Orthonormal distance between atoms (matrix multiplication)
dBA = (vBA @ g @ vBA.transpose())**0.5
dCA = (vCA @ g @ vCA.transpose())**0.5
dBC = (vBC @ g @ vBC.transpose())**0.5

# dot product between B and C (matrix multiplication)
dpBC = vBA @ g @ vCA.transpose()

##print('Metric tensor', g, sep = '\n')
##print('Distance B to A: ',str(dBA).replace('[','').replace(']',''))
##print('Distance C to A: ',str(dCA).replace('[','').replace(']',''))
##print('Distance B to C: ',str(dBC).replace('[','').replace(']',''))
##
##
##
##if np.array_equal(atomA, atomB) or np.array_equal(atomA, atomC):
##    angleCAB = 'B or C cannot equal A!'
##else:
##    angleCAB = np.rad2deg(np.arccos(dpBC / (((dBA ** 2) * (dCA ** 2)) ** 0.5)))
##
##print('Angle between B and C: ',str(angleCAB).replace('[','').replace(']',''))

no_atoms = 5

atom_list = np.random.rand(no_atoms,3)

distances = []

for atom in atom_list:
	vector = atom - atom_list
	distance =np.diagonal(np.sqrt(vector @ g @ vector.transpose()))
	distances.append(distance)

print(distances)

