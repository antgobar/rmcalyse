import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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

    x_norm = np.absolute(x_vect / vector_magnitude)
    y_norm = np.absolute(y_vect / vector_magnitude)
    z_norm = np.absolute(z_vect / vector_magnitude)

    # average vector (temporary fix, see below)
    x_av = np.mean(x_norm)
    y_av = np.mean(y_norm)

    # quarter circle points
    x = np.linspace(0, 1, 100)
    y = np.sqrt(1 - x ** 2)

    # plotting
    sns.kdeplot(x=x_norm,
                y=y_norm,
                kde=True,
                fill=True,
                levels=20,
                thresh=0.2)

    plt.scatter(x_norm, y_norm, label='data', c='darkorange', alpha=0.7)
    plt.scatter(x_av, y_av, label='average', c='red')
    plt.plot(x, y, c='k')

    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.legend()

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
