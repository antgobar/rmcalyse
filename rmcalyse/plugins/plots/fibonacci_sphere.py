import numpy as np

def fibonacci_sphere(num_pts):

	indices = np.arange(0, num_pts, dtype=float) + 0.5

	phi = np.arccos(1 - 2 * indices / num_pts)
	theta = np.pi * (1 + 5**0.5) * indices

	x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)

	points = np.array(list(zip(x, y, z)))
	
	return points
