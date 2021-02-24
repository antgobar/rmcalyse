import numpy as np
import pandas as pd


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

		# list of labels of interest
		labels_A = np.array(labels[indices_A])
		labels_B = np.array(labels[indices_B])

		self.labels_A = labels_A
		self.labels_B = labels_B

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

			# append to list 
			distances_list.append(distances)

		# create attribute & flatten list
		self.distances_list = np.array(distances_list).flatten()

	
	def make_distance_labels(self):
		# make empty list
		labels_list = []

		# nested loop to iterate through B for every A
		for label_i in self.labels_A:
			for label_j in self.labels_B:
				combined = label_i.tolist() + label_j.tolist()
				labels_list.append(combined)

		self.labels_list = labels_list


	def make_df(self):
		# column labels
		cols = ['id_A', 'atom_A','id_B', 'atom_B']
		distance_df = pd.DataFrame.from_records(self.labels_list, columns=cols)
		
		distance_df['distance'] = self.distances_list
		self.distance_df = distance_df

	def distance_window_filter(self, min_d, max_d):
		df = self.distance_df
		self.distance_df = df.loc[(df['distance'] > min_d) & (df['distance'] <= max_d)]








