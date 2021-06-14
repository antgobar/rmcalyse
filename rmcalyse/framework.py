import logging
from pathlib import Path
import glob

import numpy as np
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
        self._outputs = {}
        logger.debug(('framework successfully created with input: {}, output: {}, '
                     'and plugins = {}').format(self.input, self.output, self.plugins))
        if auto_prep:
            self.prepare_for_go()

    @classmethod
    def from_yaml(cls,yaml_file_path):
        config = load_yaml(yaml_file_path)
        return cls(config)

    def compile_outputs_dict(self):
        if not isinstance(self.plugins, list):
            logger.warning('plugins is not list, cannot iterate to find outputs')
            return
        for plugin in self.plugins:
            if isinstance(plugin, dict):
                for k,v in plugin.items():
                    if isinstance(v, dict):
                        if 'output' in v.keys():
                            output = v['output']
                            logger.debug('appending output {} to outputs'.format(output))
                            self._outputs[output] = None

    def prepare_for_go(self):
        logger.debug('prepare_for_go...')
        try:
            #input is either going to be a parquet file or a list of rmc6f files
            self.df = load_parquet_file(self.input)
        except ArrowInvalid:
            logger.debug(('file {} is not openable as a parquet file. '
                        'Opening using rmc6f reader instead').format(self.input))
            self.df, self.meta = load_rmc6f_files(self.input)
            self.compile_outputs_dict()
            self.data = self.df.drop(['label','original'], axis=1).set_index(['cell','n']).to_xarray()
            for k,v in self.meta.__dict__.items():
                if k != 'M':
                    self.data.attrs[k] = v

            self.data['xyz'] = (['v3', 'cell', 'n'], np.array((self.data.x,self.data.y, self.data.z)))

    def go(self):
        logger.debug('go...')
        for p in self.plugins:
            (p_name, p_settings), = p.items()
            logger.info('getting plugin {} with settings {}'.format(p_name, p_settings))
            plugin = PluginFactory.get_factory(p_name)(p_settings)
            try:
                _ = plugin.process(self.data, self._outputs)
                self.save()
            except Exception as e:
                logger.error('There was an unhandled error in plugin {}, {}'.format(p_name, e))
                logger.exception(e)

    def _save(self, filename):
        try:
            self.data.to_netcdf(filename, engine='netcdf4')
        except Exception as e:
            logger.error('there was a problem saving the file {}'.format(filename))
            logger.error(e)
            raise
        logger.info('file {} successfully saved.'.format(filename))
    def save(self):
        self._save(self.output)









