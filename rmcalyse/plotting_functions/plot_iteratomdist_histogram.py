import matplotlib.pyplot as plt
import numpy as np

from general_functions import interatomic_distance as iad


def iad_hist(
    orthonormal_positions,
    atomA,
    atomB,
    bin_start,
    bin_end,
    bin_size,
    combine=1
):
    '''
    Plots hystogram of interatomic distances for atoms specified in
    interatomic_distance.py function
    Returns histogram plot.
    combine: 1 or 0. (default = 1) '1' to combine histograms of all atoms,
    '0' to overlay plots of individual atom pairs
    '''

    binning = np.arange(bin_start, bin_end, bin_size).tolist()

    if combine == 1:
        hist_list = []

        iad_list = iad.interatomic_distance(orthonormal_positions, atomA, atomB, bin_start, bin_end)[0]

        for i, distance in enumerate(iad_list):
            hist_list.append(iad_list[i][10])

        # Does same as above but list comprehension
        ##hist_list = [i_a_dist_list[n][10] for n, atom in enumerate(i_a_dist_list)]

        plt.hist(hist_list, binning, label='Atom pair: {}, {}'.format(atomA, atomB))
        plt.xlabel('r (A)')
        plt.ylabel('Frequency (no. of atoms)')
        plt.legend(loc='upper left')
        plt.title('Histogram of interatomic distances')
        plt.show()

    elif combine == 0:

        histograms = []

        for i, atom in enumerate(atomA):
            for j, atom in enumerate(atomB):

                iad_list = iad.interatomic_distance(
                    orthonormal_positions,
                    atomA[i],
                    atomB[j],
                    bin_start,
                    bin_end)[0]

                histogram = [iad_list[n][10] for n, atom in enumerate(iad_list)]

                # histograms.append(histogram)

                plt.hist(histogram, binning, alpha=0.6, label='Atom pair: {}, {}'.format(atomA[i], atomB[j]))
                plt.xlabel('r (A)')
                plt.ylabel('Frequency (no. of atoms)')
                plt.legend(loc='upper left')

        plt.title('Histogram of interatomic distances')
        plt.show()

    else:
        print("No instructrion given on whether to combine histograms (1) or not (0)")

# Should this have the IAD function inside it so it hists can be
# plotted for any atom (include atom choice in iad_hist vars????


# should functions be written so they only need be called and within
# those all other dependencies are called??
