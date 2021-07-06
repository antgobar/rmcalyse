# Plugins for Developers

This is an introductory guide for developers looking to develop plugins for rmcalyse.

## Premise

A plugin is a class whose main functionality is invoked using the ```plugin.process(data, outputs, dask_handler)``` method. The framework passes three arguments to each plugin: 

| argument | description                                                  |
| -------- | ------------------------------------------------------------ |
| data    | the data as an ```xarray.Dataset``` object. This contains all the atomistic data concerning this rmcalyse run, as well as various metadata. This object should be amended in place and should not be returned. See below for a full description of the default data object. |
| outputs     | A ```dict``` linking user-defined names with various data. See below for further description. |
| daskhandler | some kind of dask handler which manages things (currently not implented anywhere) |

The plugin should return an atomistic ```dask.dataframe```object. The design intention is that any plugin only *adds* data to the atomistic ```df```, athough this is currently not enforced. The idea was that all changes should happen in-place but Dean couldn't get that to work :-|

A column in a dask dataframe needs to have a name so that plugins further down the chain can access the data. Plugins need to add a label which is sensible and unique so that future plugins can locate the correct data. The inherited ```get_column_names``` function can be used to this end, which prepends the plugin name to any iterable and returns a list of labels. 

## Prototype

Any plugin must inherit from the ```BasePlugin``` class and contain a ```process``` method:

```
from rmcalyse.plugins.base_plugin import BasePlugin

class SomethingNew(BasePlugin, plugin_name='some_new_plugin_name'):

    def process(self, data, outputs, dask_handler):
        pass
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
## Linting

Plugins can check the yaml input for conforming configuration before being called. The ```lint``` method is called to this end. the assert function should be used. Any failed assertions will be caught by the linter.:

```
    @staticmethod
    def lint(plugin_dict):
        config = plugin_dict[Centroider.name]
        for k in [CentroiderKeys.ATOM, CentroiderKeys.OUTER]:
            assert k in config.keys(), 'centroid plugin requires {} keyword'.format(k)
```

We should probably look at adding a "lint these values" function, but for the moment this is it. Remember even if you need a value in the config, you don't actually have to add it to the linter! 

## "process" Method Inputs
### data
The data as an ```xarray.Dataset``` object. This contains all the atomistic data concerning this rmcalyse run, as well as various metadata. This object should be amended in place. Once the framework loads 1 or more rmc6f files, ```data``` has the following structure:
#### Coordinates
| key | type | description |
|-----|------|-------------|
| cell | int64 | index of the cell, starting at 0 |
| n | int64 | index of the atom, starting at 0 |
#### Data Variables
| key | shape | type | description |
|-----|-------|------|-------------|
| atom | (cell,n) | object | Atomic labels as strings | 
| x | (cell,n) | float64 | atomic coordinates as read from the rmc6f file |
| y | (cell,n) | float64 | atomic coordinates as read from the rmc6f file |
| z | (cell,n) | float64 | atomic coordinates as read from the rmc6f file |
| i | (cell,n) | int64   | index of this atom in the supercell as read from the rmc6f file |
| j | (cell,n) | int64   | index of this atom in the supercell as read from the rmc6f file |
| k | (cell,n) | int64   | index of this atom in the supercell as read from the rmc6f file |
| xyz | (v3, cell, n) | float64 | a 3D matrix assembled from the x,y,z datasets |
#### Attributes
| key | description |
|-----|-------------|
| a   | RMCProfile supercell a | 
| b   | RMCProfile supercell b | 
| c   | RMCProfile supercell c | 
| al_deg   | RMCProfile supercell alpha (degrees) |
| be_deg   | RMCProfile supercell beta (degrees) |
| ga_deg   | RMCProfile supercell gamma (degrees) |
| atoms   | list of atomic species, chemical symbol as strings | 
| al   | RMCProfile supercell alpha (radians) | 
| be   | RMCProfile supercell alpha (radians) | 
| ga   | RMCProfile supercell alpha (radians) | 
| V   | Supercell volume | 
| rmcalyse_version   | version of RMCalyse which extracted this information | 

### outputs
Some plugins know by intuition alone which ```DataArray``` fields of the ```xarray.Dataset``` to work on; but some need to be told. Some plugins may work in tandem and want to communicate information which does not need to be saved or transmitted elsewhere. The management of these situations is performed by the ```outputs``` dictionary. This dict has keys that are either the user defined names from the yaml file, or potentially by plugins themselves. Any given plugin should simply amend this dict in place and should not be explicitly returned.
There is no constraint on the values held against any keys. To pass a specific xarray dataset, a string representation of the array name can be used since arrays can be retrieved using this.  
Plugins that create data for passing down the plugin chain should use keys that begin with an _ to avoid clashing with names used by users.  

```
    def process(self, data, outputs, dask_handler):
        outputs[self.config['output']] = 45
```

data can be extracted downstream using a similar syntax:

```
    def process(self, data, outputs, dask_handler):
        logger.critical(outputs[self.config['input']])
        required_data = data.get(self.config['input'])
```

### daskhandler
some kind of dask handler which manages things (currently not implented anywhere)

## Logging

If you want to feed any information back to the user, use the logging module. import the module and define a logger locally. 

```
import logging
logger = logging.getLogger(__name__)

    ....
    logger.info("the rms result was twelvty")
```

There are a number of levels of logging you can use ([see docs](https://docs.python.org/3/library/logging.html)); low ones go in to a log file, and high ones go both into the file and are directed to the screen. Currently ```info``` and higher are shown to the user (that is defined by the level of the ```s_handler``` in ```log_setup.py```).

## helpful xarray code

As a plugin developer, you will likely spend a lot of your time writing code for wrangling data out of an into the ```data``` object. Here are some helpful code snippets which you may find usefule (please feel free to suggest or add others!)

#### Get all data variables for a given atom type
```
just_oxygens_everything = data.where(data.atom=='O', drop=True) # drop means get rid of, rather than mask with nan
```
#### Get one particular data variable for a given atom type
```
just_strontium_xyz = data.xyz.where(data.atom=='Sr', drop=True)
```
#### Apply some function to each of the initial supercells individually
```
def add_a_random_number_to(data):
    n = np.random.randint(100)
    return data.x + n
data['result'] = data.groupby('cell').map(add_a_random_number_to)
```
