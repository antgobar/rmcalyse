
from .base_plugin import BasePlugin

class StereographicProjector(BasePlugin, plugin_name='stereographic'):

    def process(self, df, meta, other):
        return df

    @staticmethod
    def lint(plugin_dict):
        pass


