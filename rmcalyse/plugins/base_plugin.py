from abc import ABC, abstractmethod
import logging

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
    def __init_subclass__(cls, plugin_name='plugin_name',  **kwargs):
        super().__init_subclass__(**kwargs)
        _plugins[plugin_name] = cls
        cls.name = plugin_name

    def __init__(self, config = {}):
        self.config = config

    @staticmethod
    def lint(plugin_dictionary):
        pass

    @abstractmethod
    def process(self, df, meta, other):
        pass

    def get_required_input(self):
        return None

    @property
    def name(self):
        return self.__class__.name

class PluginFactory:
    @classmethod
    def get_factory(cls, plugin_name):
        if (plugin_name in _plugins.keys()):
            return _plugins[plugin_name]

    @classmethod
    def get_plugins(cls):
        return _plugins.keys()

