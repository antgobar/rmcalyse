import logging
from pathlib import Path
import glob

import numpy as np
import xarray as xr
from pyarrow.lib import ArrowInvalid

import rmcalyse
from rmcalyse.core.dask import load_rmc6f_files, load_parquet_file
from rmcalyse.core.readyaml import load_yaml, ConfigKeys
from rmcalyse.plugins import PluginFactory

logger = logging.getLogger(__name__)

class Framework:
    def __init__(self, config = {}, auto_prep=False):
        logger.debug('init...')
        self.config = config
        self.input = glob.glob(config.get(ConfigKeys.IN, ''))
        self.output = Path(config.get(ConfigKeys.OUT, ''))
        self.plugins = config.get(ConfigKeys.PLUGINS, [])
        self.meta = None
        self.df = None
        self._outputs = {}
        self.dask_handler = None
        self.data = None
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
            #input is either going to be a netcdf file or a list of rmc6f files
            data = xr.load_dataset(self.input)
            assert 'rmcalyse_version' in data.attrs.keys() 
            logger.info('successfully loaded data from netcdf file {}'.format(self.input))
            self.data = data
        except FileNotFoundError as e:
            logger.debug('File {} not found: {}'.format(self.input, e))
            raise
        except (OSError, AssertionError, AttributeError):
            logger.debug('File {} is not a valid rmcalyse/netcdf4 file. trying rmc6f loader...'.format(self.input))
            try:
                self._load_rmc6f_files()
            except Exception as e:
                logger.error('there was an unhandled error in loading {}'.format(self.input))

    def _load_rmc6f_files(self):
        df, meta = load_rmc6f_files(self.input)
        self.compile_outputs_dict()
        self.data = df.drop(['label','original'], axis=1).set_index(['cell','n']).to_xarray()
        for k,v in meta.__dict__.items():
            if k != 'M':
                self.data.attrs[k] = v

        self.data['xyz'] = (['v3', 'cell', 'n'], np.array((self.data.x,self.data.y, self.data.z)))
        self.data.attrs['rmcalyse_version'] = rmcalyse.__version__

    def go(self):
        logger.debug('go...')
        if self.data is None:
            logger.debug('no data in self, so running prepare_for_go')
            self.prepare_for_go()
        logger.debug('iterating plugins')
        for p in self.plugins:
            (p_name, p_settings), = p.items()
            logger.info('getting plugin {} with settings {}'.format(p_name, p_settings))
            plugin = PluginFactory.get_factory(p_name)(p_settings)
            try:
                _ = plugin.process(self.data, self._outputs, self.dask_handler)
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









