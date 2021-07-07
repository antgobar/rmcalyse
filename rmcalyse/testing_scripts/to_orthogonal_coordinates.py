# ------------------------------------------------------------------------
# 
# Program to convert atomic coordinates to orthonormal basis
# 
# ------------------------------------------------------------------------

# Lattice parameters - unit cell length and angles

# Non orthomormal basis

import numpy as np

cell = [3.998, 3.938, 3.989, 90,90.3368, 90]

a = cell[0]
b = cell[1]
c = cell[2]

al = np.deg2rad(cell[3])
be = np.deg2rad(cell[4])
ga = np.deg2rad(cell[5])

p_prime1 = np.array([[1, 0, 0]])
p_prime2 = np.array([[0, 0, 1]])

#Unit cell volume
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

p1 = M @ p_prime1.transpose()
p2 = M @ p_prime2.transpose()

distance = (sum((p1-p2)**2))**0.5

print('Distance for unit cell parameters: {},\nfrom coordinates {} to {} = {}'.format(cell, p_prime1[0], p_prime2[0], distance))
print('\nUnit cell volume = {}'.format(V))

