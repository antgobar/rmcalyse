import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from plotting_functions import plot_stereographic_projection_net as spn


def stereographic_projection(cent_vect,
                             show_points=True,
                             plot_area='full',
                             weighted=True,
                             net=True):
    '''
    Takes centroid vector outputs from centroid_calc function.
    Vectors are normalised (x,y,z components divided by magnitude of vector).
    Stereographic projection orientation is in z direction
    therefore z centroid vector not actually used.
    Normalised x and y vector components are used to plot points
    Gaussian kde module from sci stats makes density plot (points coloured by density)
    Note: vectors are all mapped to positive quadrant

    Arguments:
    cent_vetc:
        list of centroid vectors
    show_points:
        show vector points if True. If False, only kde shows
    plot_area:
        area of circle to show.
        full: z values mapped as positive 
        half: z & y vectors mapped y <= 0 quadrants
        quarter: z & y & x vectors mapped to y <= 0 and x <= quadrants
        8th: quarter collapsed into octant
    weighted:
        weighting points further from center less, avoid high point
        density at edges
    net:
        overlay stereographic projection net if True
    '''
    # Separate x y z compoents from cent_vect input (for plotting)
    x_vect = np.array([cent_vect[i][0] for i, cent in enumerate(cent_vect)])
    y_vect = np.array([cent_vect[i][1] for i, cent in enumerate(cent_vect)])
    z_vect = np.array([cent_vect[i][2] for i, cent in enumerate(cent_vect)])

    # Vector normaliseadtion
    # calculate magnitude first
    vector_magnitude = np.sqrt((x_vect**2) + (y_vect**2) + (z_vect**2))

    x_norm = x_vect / vector_magnitude
    y_norm = y_vect / vector_magnitude
    z_norm = z_vect / vector_magnitude

    # Distance from centre
    r_dist = np.sqrt(x_norm ** 2 +  y_norm ** 2)
    # Weighted by r_dist. Penalised follows inverse of semicircle function
    if weighted == True:
        weights = np.sqrt(1- r_dist ** 2)
    elif weighted == False:
        weights = None

    # conditional statements to plot full, half, quarter or eighth projection
    if plot_area == 'full':
        x = x_norm
        y = y_norm
        z = z_norm

        circle_start = -1

        plt.xlim(-1.2, 1.2)
        plt.ylim(-1.2, 1.2)

    elif plot_area == 'half':
        x = x_norm
        y = np.absolute(y_norm)
        z = z_norm

        circle_start = -1

        plt.xlim(-1.2, 1.2)
        plt.ylim(0, 1.2)

    elif plot_area == 'quarter':

        x = np.absolute(x_norm)
        y = np.absolute(y_norm)
        z = z_norm

        circle_start = 0

        plt.xlim(0, 1)
        plt.ylim(0, 1)

    elif plot_area == '8th':
        x_oct = []
        y_oct = []

        x_temp = np.absolute(x_norm)
        y_temp = np.absolute(y_norm)

        for (x, y) in zip(x_temp, y_temp):
            if y > x:
                x, y = y, x
            x_oct.append(x)
            y_oct.append(y)

        x = x_oct
        y = y_oct

        # circle plot range
        circle_start = np.cos(np.pi / 4)

        plt.xlim(0, 1)
        plt.ylim(0, 0.8)

    # average vector
    x_av = np.mean(x)
    y_av = np.mean(y)

    # circle points
    x_circle = np.linspace(circle_start, 1, 100)
    y_circle = np.sqrt(1 - x_circle ** 2)

    # KDE plot 1st (under data points)
    sns.kdeplot(x=x,
                y=y,
                fill=True,
                levels=100,
                thresh=0.2,
                weights=weights
                )

    # function argument to show points
    if show_points == True:
        plt.scatter(x, y, label='data', c='darkorange', alpha=0.7)

    # average vector
    # plt.scatter(x_av, y_av, label='average', c='red')

    #circle and line
    plt.plot(x_circle, y_circle, c='k')

    if plot_area == 'full':
        plt.plot(x_circle, -y_circle, c='k')

    if plot_area == '8th':
        plt.plot([0, circle_start], [0, max(y_circle)], c='k')

    plt.legend()

    if net == True:
        spn.sp_net(radius=1)
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.show()

