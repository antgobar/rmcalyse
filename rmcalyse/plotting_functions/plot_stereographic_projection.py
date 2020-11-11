import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def stereographic_projection(cent_vect,
                             show_points=False,
                             collapse_eighth=True):
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

    # collapse to eigth sector
    if collapse_eighth == True:
        x_oct = []
        y_oct = []

        for (x, y) in zip(x_norm, y_norm):
            if y > x:
                x, y = y, x
            x_oct.append(x)
            y_oct.append(y)

        x_norm = x_oct
        y_norm = y_oct

        # circle plot range
        circle_start = np.cos(np.pi / 4)

    else:
        circle_start = 0

    # average vector
    x_av = np.mean(x_norm)
    y_av = np.mean(y_norm)

    # circle points
    x_circle = np.linspace(circle_start, 1, 100)
    y_circle = np.sqrt(1 - x_circle ** 2)

    # plotting
    sns.kdeplot(x=x_norm,
                y=y_norm,
                kde=True,
                fill=True,
                levels=20,
                thresh=0.2)

    if show_points == True:
        plt.scatter(x_norm, y_norm, label='data', c='darkorange', alpha=0.7)

    plt.scatter(x_av, y_av, label='average', c='red')
    plt.plot([0, circle_start], [0, max(y_circle)], c='k')
    plt.plot(x_circle, y_circle, c='k')

    plt.xlim(0, 1)
    if collapse_eighth == True:
        plt.ylim(0, 0.8)

    else:
        plt.ylim(0, 1)

    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()
