# Plugins for Developers

This is an introductory guide for developers looking to develop plugins for rmcalyse.

### Premise

A plugin is a class whose main functionality is invoked using the ```plugin.process(df, meta, other)``` method. The framework passes three arguments to each plugin: 

| argument | description                                                  |
| -------- | ------------------------------------------------------------ |
| df       | the main ```dask.dataframe``` object. This contains all the atomistic data concerning this rmcalyse run. |
| meta     | the ```rmcalyse.general_functions.read_rmc6f.MetaData``` object. (this needs to move, that's a crazy place for it to live) |
| other    | dictionary of non-atomistic data that this plugin needs (see below) |

The plugin should return an atomistic ```dask.dataframe```object. The design intention is that any plugin only *adds* data to the atomistic ```df```, athough this is currently not enforced. The idea was that all changes should happen in-place but Dean couldn't get that to work :-|

A column in a dask dataframe needs to have a name so that plugins further down the chain can access the data. Plugins need to add a label which is sensible and unique so that future plugins can locate the correct data. The inherited ```get_column_names``` function can be used to this end, which prepends the plugin name to any iterable and returns a list of labels. 

### Prototype

Any plugin must inherit from the ```BasePlugin``` class and contain a ```process``` method:

```
from rmcalyse.plugins.base_plugin import BasePlugin

class SomethingNew(BasePlugin, plugin_name='some_new_plugin_name'):

    def process(self, df, meta, other):
        return df
```

you can add any other methods you require, but note the methods on the base class which you should not overwrite by accident:

```
    def lint(plugin_dictionary):
        pass

    def get_required_input(self):
        return None

    @property
    def name(self):
        return self.__class__.name
```

### Linting

Plugins can check the yaml input for conforming configuration before being called. The ```lint``` method is called to this end. the assert function should be used. Any failed assertions will be caught by the linter.:

```
    @staticmethod
    def lint(plugin_dict):
        config = plugin_dict[Centroider.name]
        for k in [CentroiderKeys.ATOM, CentroiderKeys.OUTER]:
            assert k in config.keys(), 'centroid plugin requires {} keyword'.format(k)
```

We should probably look at adding a "lint these values" function, but for the moment this is it. Remember even if you need a value in the config, you don't actually have to add it to the linter! 

### Other Data

Other data is treated in a different way. The framework contains a dictionary ```_outputs```, where the keys are the strings the user has entered next to any "output" setting in the yaml file. In the example there is just one, ```some_name``` which is output from the toy "clustering" plugin. The whole dict is passed to every plugin as the third input. Any plugin which needs to output some auxilliary data into this dict can just set it. 

```
    def process(self, df, meta, other):
        other[self.config['output']] = 45
        return df
```

data can be extracted downstream using a similar syntax:

```
    def process(self, df, meta, other):
        logger.critical(other[self.config['input']])
        return df
```

in reality, these keys 'input' and 'output' are special and should be defined somewhere in the code. We can wrap this to make it prettier if it is not overly clear how to use this. 

### Logging

If you want to feed any information back to the user, use the logging module. import the module and define a logger locally. 

```
import logging
logger = logging.getLogger(__name__)

    ....
    logger.info("the rms result was twelvty")
```

There are a number of levels of logging you can use ([see docs](https://docs.python.org/3/library/logging.html)); low ones go in to a log file, and high ones go both into the file and are directed to the screen. Currently ```info``` and higher are shown to the user (that is defined by the level of the ```s_handler``` in ```log_setup.py```).

### Working on individual configurations

The atomistic dataframe ```framework.df``` contains all the rmc6f files which are included. Some plugins will want to process these seperately. You can use the ```cell``` column for this purpose. 

```
>>> f.df.shape[0].compute()
50000
>>> f.df[f.df['cell'] == 3].shape[0].compute()
5000
```

Just realised it would be useful for the framework to know how many cells there are as a property, so I'll also add that to my to-do list. 
