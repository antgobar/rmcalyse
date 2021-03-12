
from .base_plugin import BasePlugin

class Clusterer(BasePlugin, plugin_name='clustering'):

    def process(self, df, meta, other):
        other[self.config['output']] = 45
        return df

    @staticmethod
    def lint(plugin_dict):
        pass


