import numpy as np
import matplotlib.pyplot as plt


def vector_hist(cent_vect):
    '''
    Takes list of centroid vectors from centroid_vector module and
    plots histogram of vector magnitudes
    '''
    binwidth = 0.02

    list_lengths = [np.sqrt(np.dot(vector, vector)) for vector in cent_vect]

    bins = np.arange(min(list_lengths), max(list_lengths) + binwidth, binwidth)

    plt.hist(list_lengths, bins)
    plt.title('Histograms of offcentering vectors')

    plt.show()
