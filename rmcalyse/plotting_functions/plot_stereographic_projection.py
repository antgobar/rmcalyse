import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def stereographic_projection(cent_vect):
    '''
    Takes centroid vector outputs from centroid_calc function.
    Vectors are normalised (x,y,z components divided by magnitude of vector).
    Stereographic projection orientation is in z direction 
    therefore z centroid vector not actually used.
    Normalised x and y vector components are used to plot points 
    Gaussian kde module from sci stats makes density plot (points coloured by density)
    Note: vectors are all mapped to positive quadrant
    '''
    # Separate x y z compoents from cent_vect input (for plotting)
    x_vect = np.array([cent_vect[i][0] for i, cent in enumerate(cent_vect)])
    y_vect = np.array([cent_vect[i][1] for i, cent in enumerate(cent_vect)])
    z_vect = np.array([cent_vect[i][2] for i, cent in enumerate(cent_vect)])
    
    # magnitude used for normalisation
    vector_magnitude = np.sqrt((x_vect**2) + (y_vect**2) + (z_vect**2))
    
    x_norm = np.absolute(x_vect/vector_magnitude)
    y_norm = np.absolute(y_vect/vector_magnitude)
    z_norm = np.absolute(z_vect/vector_magnitude)
    
    
    # Calculate the point density, note z_norm not used here
    xy = np.vstack([x_norm,y_norm])
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    ax.scatter(x_norm, y_norm, c=z, s=200, edgecolor='')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
