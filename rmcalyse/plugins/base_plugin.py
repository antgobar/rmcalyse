from abc import ABC, abstractmethod
import loggging

from rmcalyse.core.hdfstore import HDFS
_plugins = {}

class BasePlugin(ABC):
    """A base plugin for rmcalyse.

    A plugin is instantiated with some configuration and a string describing the plugin
    which saved the data that we want this plugin to work on
    Then the process method is called with the path to a pandas HDFStore as the only
    necessary argument
    The plugin then does whatever it is designed and configured to do
    This may include creating output files
    This may include appending information to the hdf5 file
    """

    @classmethod
    def __init_subclass__(cls, name='plugin_name', is_abstract=False, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_abstract:
            _plugins[name] = cls

    @abstractmethod
    def __init__(self, use_output_from = 'previous_plugin_name', config = {}):
        self.use_output_from = use_output_from
        self.config = config

    @abstractmethod
    def _process(self, data):
        pass

    def process(self, path_to_hdf):
        self._hdfs = HDFS(self.name, self.use_output_from, path_to_hdf)
        for i,data in enumerate(self._hdfs):
            result = self._process(data)
            self.write(i, result)

    def write(self, i, data):
        if data is not None:
            self._hdfs.write(i, data)



class PluginFactory:
    @classmethod
    def get_factory(cls, plugin_name, previous_plugin_name, config):
        if (plugin_name in _plugins.keys()):
            return _plugins[plugin_name](previous_plugin_name, config)

    @classmethod
    def get_plugins(cls):
        return _plugins.keys()

