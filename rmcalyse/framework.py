import logging
from pathlib import Path
import glob

from pyarrow.lib import ArrowInvalid

from rmcalyse.core.dask import load_rmc6f_files, load_parquet_file
from rmcalyse.core.readyaml import load_yaml, ConfigKeys
from rmcalyse.plugins import PluginFactory

logger = logging.getLogger(__name__)

class Framework:
    def __init__(self, config = {}, auto_prep=True):
        logger.debug('init...')
        self.config = config
        self.input = glob.glob(config.get(ConfigKeys.IN, ''))
        self.output = Path(config.get(ConfigKeys.OUT, ''))
        self.plugins = config.get(ConfigKeys.PLUGINS, [])
        self.meta = None
        self.df = None
        logger.debug(('framework successfully created with input: {}, output: {}, '
                     'and plugins = {}').format(self.input, self.output, self.plugins))
        if auto_prep:
            self.prepare_for_go()

    @classmethod
    def from_yaml(cls,yaml_file_path):
        config = load_yaml(yaml_file_path)
        return cls(config)

    def prepare_for_go(self):
        logger.debug('prepare_for_go...')
        try:
            #input is either going to be a parquet file or a list of rmc6f files
            self.df = load_parquet_file(self.input)
        except ArrowInvalid:
            logger.debug(('file {} is not openable as a parquet file. '
                        'Opening using rmc6f reader instead').format(self.input))
            self.df, self.meta = load_rmc6f_files(self.input)

    def go(self):
        logger.debug('go...')
        for p in self.plugins:
            (p_name, p_settings), = p.items()
            logger.info('getting plugin {} with settings {}'.format(p_name, p_settings))
            plugin = PluginFactory.get_factory(p_name)(p_settings)
            required_input = plugin.get_required_input()
            try:
                self.df = plugin.process(self.df, self.meta, required_input)
            except Exception as e:
                logger.error('There was an unhandled error in plugin {}, {}'.format(p_name, e))
                logger.exception(e)











