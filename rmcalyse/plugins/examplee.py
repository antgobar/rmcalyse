import logging
import numpy as np

from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class Examplere(BasePlugin, plugin_name='examplee'):

    def process(self,data, outputs, dask_handler):
        logger.info("outputs: {}".format(outputs))
        logger.info("cionfig: {}".format(self.config))
        data['something'] = np.arange(100)
        outputs['cheese'] = 'something'

    @staticmethod
    def lint(plugin_dict):
        config = plugin_dict[Examplere.name]
        assert "atom_were_inteerested_in" in config.keys(), "examplee needs atom_were_inteerested_in"


