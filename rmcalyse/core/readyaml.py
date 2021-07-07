import inspect
import logging
import yaml
import glob

from rmcalyse.plugins import PluginFactory

logger = logging.getLogger(__name__)

def load_yaml(filepath):
    with open(filepath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)
    linter = ConfigLinter(config)
    if linter.lint():
        logger.info('yaml successfully linted')
    return config

class ConfigKeys:
    IN = 'input'
    OUT = 'output'
    PLUGINS = 'plugins'

class ConfigLinter:
    def __init__(self,config):
        self.config = config

    @staticmethod
    def _run_linting_function(f, *args, **kwargs):
        try:
            f(*args, **kwargs)
            return True
        except AssertionError as e:
            logger.error(e)
            return False

    @staticmethod
    def _check_plugin_exists(plugin_name):
        assert plugin_name in PluginFactory.get_plugins(), \
                "plugin '{}' not found".format(plugin_name)

    def lint(self):
        good = True
        for n,f in inspect.getmembers(self, predicate=inspect.ismethod):
            if not n.startswith('check'):
                continue
            good = good and ConfigLinter._run_linting_function(f)

        if good:
            logger.debug('Configuration successfully linted')
            logger.debug(self.config)
        else:
            logger.warning('Configuration linting failure')
        return good

    def check_input_exists(self):
        assert ConfigKeys.IN in self.config.keys(), \
                '{} is a required config key'.format(ConfigKeys.IN)

    def check_inputs(self):
        file_list = glob.glob(self.config[ConfigKeys.IN])
        assert len(file_list) > 0, \
                'No files matching {} found'.format(self.config[ConfigKeys.IN])

    def check_output(self):
        assert ConfigKeys.OUT in self.config.keys(), \
                '{} is a required config key'.format(ConfigKeys.OUT)

    def check_plugins(self):
        assert ConfigKeys.PLUGINS in self.config.keys(), \
                '{} is a required config key'.format(ConfigKeys.PLUGINS)

    def check_plugins_are_list(self):
        assert isinstance(self.config[ConfigKeys.PLUGINS], list), \
                'plugins need to start with - in yaml file'

    def check_plugins_are_non_zero(self):
        assert len(self.config[ConfigKeys.PLUGINS]) > 0, \
                'should be more than 0 plugins'

    def check_plugins_are_dicts(self):
        for p in self.config[ConfigKeys.PLUGINS]:
            assert isinstance(p, dict), \
                    'plugins should be dicts, error with {} '.format(p)

    @staticmethod
    def get_plugin_keys(plugin):
        try:
            return plugin.keys()
        except AttributeError as e:
            logger.error(e)
            s = ('there was a problem linting plugin {}. '
                 'Check the formatting of the yaml file.').format(plugin)
            logger.error(s)
            return []

    def check_plugin_formatting(self):
        for p in self.config[ConfigKeys.PLUGINS]:
            try:
                assert len(ConfigLinter.get_plugin_keys(p)) > 0, \
                        'plugin {} not formtted correctly. Check the yaml formatting'.format(p)
                assert len(ConfigLinter.get_plugin_keys(p)) < 2, \
                        'plugin {} has too many keys'.format(p)
            except AttributeError as e:
                logger.error(e)
                s = ('there was a problem linting plugin {}. '
                    'Was a colon missing from the yaml?').format(p)
                logger.error(s)


    def check_plugin_linters(self):
        for p in self.config[ConfigKeys.PLUGINS]:
            pname = list(ConfigLinter.get_plugin_keys(p))[0]
            Plugin = PluginFactory.get_factory(pname)
            try:
                Plugin.lint(p)
            except AttributeError:
                assert False,  "plugin '{}' not found".format(pname)
    def check_plugin_inputs_have_outputs(self):
        plugins = self.config[ConfigKeys.PLUGINS]
        inputs = []
        outputs = []
        for plugin in plugins:
            if isinstance(plugin, dict):
                for k,v in plugin.items():
                    if isinstance(v, dict):
                        if 'input' in v.keys():
                            inputs.append(v['input'])
                        if 'output' in v.keys():
                            outputs.append(v['output'])

        assert all([inp in outputs for inp in inputs]), \
                ('one or more inputs ({}) not specified '
                'by any of the outputs ({})').format(inputs, outputs)
