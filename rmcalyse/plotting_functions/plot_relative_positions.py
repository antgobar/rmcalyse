import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_rel_pos(rel_position, atomA, atomB):
    '''
    Takes relative positions from interatomic_distance[1] function
    Creates x y z lits of coordinates to be plotted
    '''
    x_position = [0]  # first point is at 0, 0, 0.
    y_position = [0]
    z_position = [0]

    for i, coords in enumerate(rel_position):
        x_position.append(rel_position[i][0])
        y_position.append(rel_position[i][1])
        z_position.append(rel_position[i][2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_position, y_position, z_position, c='r', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Atom pair: {}, {}'.format(atomA[:], atomB[:]))

    # Plot data
    plt.show()
