import logging
import numpy as np

from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class Exampler(BasePlugin, plugin_name='example'):

    def process(self,data, outputs):

        # get one type of atom:
        just_oxygens_everythin = data.where(data.atom=='O', drop=True) # drop means get rid of, rather than mask with nan
        logger.debug(just_oxygens_everythin)
        just_strontium_xyz = data.xyz.where(data.atom=='Sr', drop=True)
        logger.debug(just_strontium_xyz)

        #do something on a cell-by-cell basis and put back in
        def add_a_random_number_to(data):
            n = np.random.randint(100)
            return data.x + n
        data['result'] = data.groupby('cell').map(add_a_random_number_to)


    @staticmethod
    def lint(plugin_dict):
        pass


