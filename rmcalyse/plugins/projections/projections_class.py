import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Projection():

	def __init__(self, centroid_vector):

		self.centroid_vector = centroid_vector

		# magnitudes
		self.magnitude = np.linalg.norm(self.centroid_vector, axis = 1)

		# x y z components
		self.x = self.centroid_vector[:, 0]
		self.y = self.centroid_vector[:, 1]
		self.z = self.centroid_vector[:, 2]

		# x y z normalised to magnitude
		self.x_norm = self.x / self.magnitude
		self.y_norm = self.y / self.magnitude
		self.z_norm = self.z / self.magnitude


	def orthographic_projection(self):
		x, y = self.x_norm, self.y_norm
		return x, y


	def stereographic_projection(self):
		x = 2 * self.x_norm / (self.z_norm + 1)
		y = 2 * self.y_norm / (self.z_norm + 1)
		return x, y


	def lambert_azimuzal_projection(self):
		pass
