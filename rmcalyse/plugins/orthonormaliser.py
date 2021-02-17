
from .base_plugin import BasePlugin

class Orthonormaliser(BasePlugin, plugin_name='orthonormaliser'):
    def __init__(self, use_output_from, config):
        super().__init__(use_output_from, config)

    def _process(self, data):
        # here data is going to be whatever is returned by read_hdfstore, probably a df
        data += 1


