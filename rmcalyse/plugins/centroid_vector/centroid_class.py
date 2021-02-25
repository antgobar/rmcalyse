import numpy as np
import pandas as pd


class Centroid():

	def __init__(self, labels, positions):
		self.labels = labels
		self.positions = positions


	def get_centroid_vectors(self, atomA, atomB, coordination_number, matrix):

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

		# list of labels of interest
		labels_A = np.array(labels[indices_A])
		labels_B = np.array(labels[indices_B])

		# predefine results array for speed
		self.centroid_vectors = np.zeros((positions.shape[0],3)) 

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

			# returns an array indices sorted by distance
			sorted_indices = np.argsort(distances) 
			
			# ordered orthonormal distances
			ordered_orthonormalised_positions = orthonormalised[sorted_indices]

			# select smallest n where n is coordination number
			coordinating_orthonormal_positions = ordered_orthonormalised_positions[ : coordination_number]

			# average position (centroid) of the coordination atoms
			centroid = np.mean(coordinating_orthonormal_positions, axis = 0)
			
			# populate atribute: centroids array at index of interest
			# the remaining indices will be 0
			self.centroid_vectors[index,:] = -centroid

		self.non_zero_vectors = self.centroid_vectors[np.linalg.norm(self.centroid_vectors,  axis = 1) > 0]



