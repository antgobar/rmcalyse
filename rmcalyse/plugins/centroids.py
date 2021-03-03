
from .base_plugin import BasePlugin

class CentroiderKeys:
    ATOM = 'atom'
    OUTER = 'outer'

class Centroider(BasePlugin, plugin_name='centroid'):

    def process(self, df, meta, other_data):
        df['new_column'] = df['x'] + df['y'] + df['z']
        return df

    @staticmethod
    def lint(plugin_dict):
        config = plugin_dict[Centroider.name]
        for k in [CentroiderKeys.ATOM, CentroiderKeys.OUTER]:
            assert k in config.keys(), 'centroid plugin requires {} keyword'.format(k)



