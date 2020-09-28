import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_supercell(orthonormal_positions, atoms2plot):

    op = orthonormal_positions

    '''
    Plot all (or only desired) atoms in orthormalised supercell 
    '''

    # This is required to filter out atoms which want plotting.
    # If done after causes some issues with aligning atoms to their coordiantes..?
    to_plot = [op[i][:] for i, atom in enumerate(op) if op[i][0] in atoms2plot]

    scatter_x = np.array([to_plot[i][2] for i, atom in enumerate(to_plot)])
    scatter_y = np.array([to_plot[i][3] for i, atom in enumerate(to_plot)])
    scatter_z = np.array([to_plot[i][4] for i, atom in enumerate(to_plot)])

    group = np.array([to_plot[i][0] for i, atom in enumerate(to_plot)])

    color_list = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
    cdict = dict(zip(atoms2plot, color_list))  # connect atoms to colours

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for g in np.unique(group):
        ix = np.where(group == g)
        ax.scatter(
            scatter_x[ix],
            scatter_y[ix],
            scatter_z[ix],
            c=cdict[g],
            label=g,
            s=50,  # size
            alpha=1)  # opaqueness

    ax.legend(loc='upper right')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Orthonormalised supercell')
    plt.show()

    return group
