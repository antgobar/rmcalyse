
from .base_plugin import BasePlugin

class VolumePlotter(BasePlugin, plugin_name='volume_plot'):

    def process(self, df, meta, other):
        return df

    @staticmethod
    def lint(plugin_dict):
        pass


