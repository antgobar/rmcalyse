import numpy as np
import matplotlib.pyplot as plt

def sp_net(radius):
    '''
    function which creates a crystallographic orientation net
    to overlay on stereographic projection plots
    plt.show() should be commented out
    '''
    base_angle = np.linspace(-90, 90, 100)
    base_length = 1 / np.cos(base_angle * np.pi / 180)
    angle2point = (180 / np.pi) * np.arctan(1/base_length)
    angle_inner = 45 - angle2point* 0.5
    opposite = radius * np.tan(angle_inner * np.pi / 180)

    x = opposite * np.cos(base_angle * np.pi / 180)
    y = opposite * np.sin(base_angle * np.pi / 180)

    diag = radius * np.cos(np.pi/4)
    diag_m = np.linspace(-diag, diag)

    orth = np.linspace(-radius, radius, 2)

    plt.plot(x, y, c='k')
    plt.plot(-x, y, c='k')
    plt.plot(y, x, c='k')
    plt.plot(y, -x, c='k')

    plt.plot(diag_m, diag_m, c='k')
    plt.plot(diag_m, -diag_m, c='k')

    plt.plot(np.zeros(2), orth, c='k')
    plt.plot(orth, np.zeros(2), c='k')

    circle1 = plt.Circle((0, 0), radius, color='k', fill = False)
    plt.gca().add_patch(circle1)

    plt.gca().set_aspect('equal', adjustable='box')
    #plt.show()
