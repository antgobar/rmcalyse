import logging

from .base_plugin import BasePlugin
from ..core.orthonormlise import orthonormalise_distance_to_origin

logger = logging.getLogger(__name__)

class CentroiderKeys:
    CENTRAL = 'central'
    OUTER = 'outer'
    R_MIN = 'r_min'
    COORD = 'coordination'


class Centroider(BasePlugin, plugin_name='centroid'):

    def process(self, df, meta, other):
        #for cell in meta.cells:
        #self.config
        positions = df[['x', 'y', 'z']].to_dask_array()

        offset = 0.5
        positions -= offset # now the unit cell goes from -19 to 19
        return df
        #idx_of_interest = [i for i,x in enumerate(orthonormal_positions) if x[0] in center_atom] # hack to find a list of indices we're interested in
        #make this work
        #results = np.zeros((positions.shape[0],3)) # predefine results array for speed
        #logger.debug('startign the loop')
        #for i in idx_of_interest:
        #    shifted = (positions - positions[i]) #shift all atoms so this one is at the origin
        #    reshuffled = np.mod(shifted+offset, offset*2)-offset # the clever moving of atoms outside -19:19 back
        #    distances = orthonormalise_distance_to_origin(reshuffled, meta.M)
        #    idx = np.argsort(distances) # returns an array of sorted indices (i.e. distances[idx[0]] = 0, the distance from the atom to itself, distances[idx[1]] is somewthing like 2.5, etc.
        #    results[i,:] = -np.mean(reshuffled[idx[1:7], :],0) #note we start at 1 to avoid the 0 for the same atom. Then average them. this calculates the central point so the displacements vector is -ve this



        # put the results bacvk in t6he datavradmenwegh b

    



        return df
