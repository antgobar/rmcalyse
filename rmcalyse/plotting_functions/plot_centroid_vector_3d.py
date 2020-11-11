import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def centroid_vector_plot(cent_vect, centroid, atomA, atomB):
    '''
    Plot 3D vector field of vectors describing the off centering of
    center atom relative to centroid of orbit atoms
    '''

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Centroid coordinates i.e. origin of centroid vectors
    # or off-centereeing vectors
    x_centroid = [centroid[i][0] for i, cent in enumerate(centroid)]
    y_centroid = [centroid[i][1] for i, cent in enumerate(centroid)]
    z_centroid = [centroid[i][2] for i, cent in enumerate(centroid)]

    # Centroid_vector or off-centering vectors.
    x_cent_vect = [cent_vect[i][0] for i, cent in enumerate(cent_vect)]
    y_cent_vect = [cent_vect[i][1] for i, cent in enumerate(cent_vect)]
    z_cent_vect = [cent_vect[i][2] for i, cent in enumerate(cent_vect)]

    ##vect_len = [np.sqrt(i.dot(i)) for i in cent_vect]

    ax.quiver(
        x_centroid,
        y_centroid,
        z_centroid,
        x_cent_vect,
        y_cent_vect,
        z_cent_vect,
        length=5,
        color='blue'
    )

    # NET VECTOR OVERLAY ON PLOT
    # average position of all centroids (should be approx center of plot)
    # Net vector will be overlayed in center of cell
    x_av = np.average([centroid[i][0] for i, cent in enumerate(centroid)])
    y_av = np.average([centroid[i][1] for i, cent in enumerate(centroid)])
    z_av = np.average([centroid[i][2] for i, cent in enumerate(centroid)])

    # sum of all centroid vectors
    x_mag = np.sum([cent_vect[i][0] for i, vec in enumerate(cent_vect)])
    y_mag = np.sum([cent_vect[i][1] for i, vec in enumerate(cent_vect)])
    z_mag = np.sum([cent_vect[i][2] for i, vec in enumerate(cent_vect)])

    ax.quiver(
        x_av,
        y_av,
        z_av,
        x_mag,
        y_mag,
        z_mag,
        length=2,
        color='red'
    )

    x_net = round(x_mag, 3)
    y_net = round(y_mag, 3)
    z_net = round(z_mag, 3)

    min_net_vect = min([x_net, y_net, z_net])

    normalised_net_vect_x = round(x_net / min_net_vect, 3)
    normalised_net_vect_y = round(y_net / min_net_vect, 3)
    normalised_net_vect_z = round(z_net / min_net_vect, 3)

    plt.title('''Atom pairs: {}, {} \n Net displacement vector:\n x={} y={} z={}'''
              .format(atomA[:],
                      atomB[:],
                      normalised_net_vect_x,
                      normalised_net_vect_y,
                      normalised_net_vect_z))

    plt.show()

    return [x_mag, y_mag, z_mag]
