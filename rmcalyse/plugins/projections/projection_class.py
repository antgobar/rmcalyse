import numpy as np

class Projection():

	def __init__(self, vectors):

		self.vectors = vectors

		# magnitudes
		self.magnitudes = np.linalg.norm(self.vectors, axis = 1).reshape(len(self.vectors), 1)

		# normalised vectorss
		self.norm_vectors = self.vectors / self.magnitudes
		
		# x y z components
		self.x = self.vectors[:, 0]
		self.y = self.vectors[:, 1]
		self.z = self.vectors[:, 2]

		# x y z normalised to magnitudes
		self.x_norm = self.norm_vectors[:, 0]
		self.y_norm = self.norm_vectors[:, 1]
		self.z_norm = self.norm_vectors[:, 2]


	def orthographic_projection(self):
		
		x, y = self.x_norm, self.y_norm
		
		return x, y


	def stereographic_projection(self):
		
		x = 2 * self.x_norm / (np.absolute(self.z_norm) + 1)
		y = 2 * self.y_norm / (np.absolute(self.z_norm) + 1)
		
		return x, y


	def lambert_azimuthal_projection(self):
		
		# 1 - z coordinate
		z_up = 1 - np.absolute(self.z_norm)

		# projected vector magnitude
		r  = np.sqrt(self.x_norm ** 2 + self.y_norm ** 2 + z_up ** 2)
		
		# ratio multiplyer
		k =  r / np.sqrt(self.x_norm ** 2 + self.y_norm ** 2)

		x = self.x_norm * k
		y = self.y_norm * k
		
		return x, y

