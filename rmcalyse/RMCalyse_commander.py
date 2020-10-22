###=====================================================================
###___________________________IMPORT MODULES____________________________
###---------------------------------------------------------------------

from general_functions import (read_rmc6f as rr,
                               orthonormalise as on,
                               distance_calculator as dc,
                               interatomic_distance as iad,
                               average_cell as ac,
                               centroid_vector as cv)

from plotting_functions import (plot_supercell as ps,
                                plot_iteratomdist_histogram as pih,
                                plot_relative_positions as prp,
                                plot_centroid_vector_histogram as cvh,
                                plot_centroid_vector_3d as cv3d,
                                plot_stereographic_projection as sp)

###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###_____________________CONFIGURATION PARAMETERS________________________
###---------------------------------------------------------------------

file_in = 'read_in/SrTiO3_00Nb.rmc6f'
atomA = ['Sr']
atomB = ['Ti']
min_d = 2   # Min range for distance calculations (if = 0 distance to
            # itself will be included in the histogram!)
max_d = 4   # For centroid vector this <= than nearest neghbour
centroid_shell_d = 4 # max distance for centroid polyhedra
coord_no = 8  # Coordination number for centroid calc
hist_bin_size = 0.05 # Histogram bin size...
combine = 0 # 0 = histograms from more than one atom-pair are overlayed
            # 1 = histograms are combined into one
atoms2plot = ['Sr', 'Ti'] # Atoms to plot in supercell plot function
atom4av_cell = 'Ti' # Atom choice from which to calculate average
                    # perovskite cell parameter

###---------------------------------------------------------------------
###=====================================================================

###=====================================================================
###__________________________CALL FUNCITONS_____________________________
###---------------------------------------------------------------------

rmc6f_data = rr.read_in(file_in)
cell, atom_list = rmc6f_data

op= on.orthonormalise(cell, atom_list)

group = ps.plot_supercell(op, atoms2plot)

distances, relative_positions = \
    iad.interatomic_distance(op, atomA, atomB, min_d, max_d)

average_param = ac.av_unit_cell(op, atom4av_cell, 4.5)

pih.iad_hist(op, atomA, atomB, min_d, max_d, hist_bin_size, combine)

cent_vect, centroid = \
    cv.centroid_calc(op, atomA, atomB, centroid_shell_d, coord_no)

sp.stereographic_projection(cent_vect)

cvh.vector_hist(cent_vect)

net_vect = cv3d.centroid_vector_plot(cent_vect, centroid, atomA, atomB)

prp.plot_rel_pos(relative_positions, atomA, atomB)

###---------------------------------------------------------------------
###=====================================================================
