
from .base_plugin import BasePlugin

class Clusterer(BasePlugin, plugin_name='clustering'):

    def process(self, df, meta, other):
        return df

    @staticmethod
    def lint(plugin_dict):
        pass


