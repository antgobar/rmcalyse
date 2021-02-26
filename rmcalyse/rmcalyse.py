### Main File ###
import numpy as np
import pandas as pd
# core imports
from core import rmcalyse_welcome
from core.supercell_class import SuperCell

# plugin imports
from plugins.distance_calculations.distance_class import Distance
from plugins.centroid_vector.centroid_class import Centroid
from plugins.projections.projection_class import Projection
from plugins.plots.plot_projections import plot_projections
from plugins.plots.fibonacci_sphere import fibonacci_sphere

# file path
file_path = 'read_in/SrTiO3_30Nb_SCARF.rmc6f'

# create rmc object
rmc_data = SuperCell(file_path)

# fetch data from rmc6f file
rmc_data.get_data()
df = pd.DataFrame.from_records(rmc_data.atom_list, columns=rmc_data.position_list_header)
rmc_data.orthonormalise_cell()


rmc_centroid = Centroid(rmc_data.position_labels, rmc_data.raw_basis_positions)
rmc_centroid.get_centroid_vectors('Sr','Ti', 8, rmc_data.matrix)

vectors = rmc_centroid.non_zero_vectors


to_project = Projection(vectors)

# all normalised vector magnitudes should be 1!
print(np.linalg.norm(to_project.norm_vectors, axis =1))


# x, y = to_project.lambert_azimuthal_projection()

# weights = to_project.magnitudes.reshape(len(to_project.magnitudes),)

# plot_projections(x, y, weighting=weights, show_points=True)


####
# points = fibonacci_sphere(500)

# sphere = Projection(points)

# x, y = sphere.orthographic_projection()
# plot_projections(x, y, show_points=True)

# x, y = sphere.stereographic_projection()
# plot_projections(x, y, show_points=True)

# x, y = sphere.lambert_azimuthal_projection()
# plot_projections(x, y, show_points=True)


