import pandas as pd
import logging

from rmcalyse.core.constants import KEYS

logger = logging.getLogger(__name__)

class HDFS:
    def __init__(self, plugin_name, use_output_from, path_to_hdf):
        self.plugin_name = plugin_name
        self.use_output_from = use_output_from
        self.path_to_hdf = path_to_hdf

    @property
    def meta(self):
        with pd.HDFStore(self.path_to_hdf) as h:
            try:
                return h[KEYS.META]
            except KeyError:
                logger.warn('no meta found in file')

    @property
    def keys(self):
        with pd.HDFStore(self.path_to_hdf) as h:
            return h.keys()

    @property
    def n_frames(self):
        with pd.HDFStore(self.path_to_hdf) as h:
            return len([x for x in h.keys() if x.startswith(KEYS.RAW)])

    def __iter__(self):
        return HDFStoreIterator(self)

    def write(self, )

class HDFSIterator:
    def __init__(self, hdfs):
        self.hdfs = hdfs
        self.index = 0
        self.n = 0
    def __next__(self):
        if self.hdfs.n_points == 0:
            logger.warn('Iterating over hdfstore with no data points')
        if self.index == 0:
            #this is the first one, so store n_points
            self.n = self.hdfs.n_points
        if self.index < self.n:
            result = self.hdfs.read_frame(self.index)
            self._index += 1
            return result
        raise StopIteration
