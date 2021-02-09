import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.gca(projection='3d')

x_pos = [0, 0, 0]
y_pos = [0, 0, 0]
z_pos = [0, 0, 0]
x_direct = [2, 0, 0]
y_direct = [0, 1, 0]
z_direct = [0, 0, 1]


ax.quiver(
    x_pos,
    y_pos,
    z_pos,
    x_direct,
    y_direct,
    z_direct,
    length=0.05)

plt.show()
