###------------------------------------------------------------------------
###
### Program to copute interatomic distances from a non-orthonomal basis
###
###------------------------------------------------------------------------

# Import relevant libraries

import numpy as np
import os


# Lattice parameters - unit cell length and angles
a = 9.503044
b = 5.52558
c = 5.59397

al = np.deg2rad(89.826400)
be = np.deg2rad(125.757286)
ga = np.deg2rad(89.927844)


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

print('Metric tensor', g, sep = '\n')
print('Distance B to A: ',str(dBA).replace('[','').replace(']',''))
print('Distance C to A: ',str(dCA).replace('[','').replace(']',''))
print('Distance B to C: ',str(dBC).replace('[','').replace(']',''))



if np.array_equal(atomA, atomB) or np.array_equal(atomA, atomC):
    angleCAB = 'B or C cannot equal A!'
else:
    angleCAB = np.rad2deg(np.arccos(dpBC / (((dBA ** 2) * (dCA ** 2)) ** 0.5)))

print('Angle between B and C: ',str(angleCAB).replace('[','').replace(']',''))

