import logging

from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class VolumePlotter(BasePlugin, plugin_name='volume_plot'):

    def process(self, df, meta, other):
        logger.critical(other[self.config['input']])
        return df

    @staticmethod
    def lint(plugin_dict):
        pass


