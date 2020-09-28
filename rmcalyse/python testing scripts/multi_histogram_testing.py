import random
import numpy as np
import matplotlib.pyplot as plt

##x = [random.gauss(3,1) for _ in range(400)]
##y = [random.gauss(4,2) for _ in range(400)]
##
##bins = np.linspace(-10, 10, 100)
##
##plt.hist(x, bins, alpha=0.5, label='x')
##plt.hist(y, bins, alpha=0.5, label='y')
##plt.legend(loc='upper left')
##plt.title('Title 1')
##plt.title('Title 2')
# plt.show()

import interatomic_distance as iad
from RMCalyse_commander import orthonormal_positions

atomA = ['Pb', 'Bi', 'Na']
atomB = ['Ti']
min_d = 2.5
max_d = 4
bin_size = 0.1
bin_start, bin_end = min_d, max_d

binning = np.arange(bin_start, bin_end, bin_size).tolist()

histograms = []

for i, atom in enumerate(atomA):
    for j, atom in enumerate(atomB):

        iad_list = iad.interatomic_distance(orthonormal_positions, atomA[i], atomB[j], bin_start, bin_end)[0]
        histogram = [iad_list[n][10] for n, atom in enumerate(iad_list)]

        # histograms.append(histogram)

        plt.hist(histogram, binning, alpha=0.6, label='Atom pair: {}, {}'.format(atomA[i], atomB[j]))
        plt.xlabel('r (A)')
        plt.ylabel('Frequency (no. of atoms)')
        plt.legend(loc='upper left')

plt.title('Histogram of interatomic distances')
plt.show()

# for hist in histograms:
##    plt.hist(hist, binning, label = 'Atom pair: {}, {}'.format(atomA, atomB))
##    plt.xlabel('r (A)')
##    plt.ylabel('Frequency (no. of atoms)')
##    plt.legend(loc='upper left')
##    plt.title('Histogram of interatomic distances')
# plt.show()
