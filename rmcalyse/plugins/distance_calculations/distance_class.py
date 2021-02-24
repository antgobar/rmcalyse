import numpy as np

class Distance():

	def __init__(self, labels, positions):
		self.labels = labels
		self.positions = positions

	def array_distance_orthonormaliser(self, atomA, atomB, matrix):

		positions = self.positions
		labels = self.labels

		# half unit cell offset
		offset = 0.5

		# cell center placed at [0, 0, 0] i.e. 
		# cell goes for -0.5 : 0.5
		positions -= offset

		# indices of interest based on atomA and atomB coices
		indices_A = [i for i, x in enumerate(positions) if labels[i][1] in atomA]
		indices_B = [i for i, x in enumerate(positions) if labels[i][1] in atomB]

	    # empty lists to fill
		distances_list = []

		# loop through atomA
		for index in indices_A:
	        
			# shift all atoms"B" so atom A is at origin
			shifted = (positions[indices_B] - positions[index]) 

			# the clever moving of atoms outside -0.5:0.5
			reshuffled = np.mod(shifted + offset, offset * 2) - offset 

			# orthonormalisation step
			orthonormalised = np.dot(matrix, reshuffled.T).T

			# calculate distances
			distances  = np.power(np.square(orthonormalised).sum(1), 0.5) 

			distances_list.append(distances)
			
			self.distances_list = np.array(distances_list).flatten()



