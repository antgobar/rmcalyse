import dask.dataframe as dd
import pandas as pd
import numpy as np

import glob
import xarray as xr

from rmcalyse.log_setup import add_logging_handlers
from rmcalyse.framework import Framework
from rmcalyse.core.dask import _load_rmc6f_file

f = Framework.from_yaml('rmcalyse/input.yaml')
g = Framework.from_yaml('rmcalyse/input_example.yaml')


"""
for inp in f.input:
    df, me, ml = _load_rmc6f_file(inp)



temp = 15 + 8 * np.random.randn(2, 2, 3)
precip = 10 * np.random.rand(2, 2, 3)
something_new = np.random.rand(2,2,6)

lon = [[-99.83, -99.32], [-99.79, -99.23]]
lat = [[42.25, 42.21], [42.63, 42.59]]
new_axis = [2,3,4,6,7,8]
ds = xr.Dataset(
    {
        "temperature": (["x", "y", "time"], temp),
        "precipitation": (["x", "y", "time"], precip),
        "tensor": (["x","y","new"], something_new)
    },
    coords={
        "lon": (["x", "y"], lon),
        "lat": (["x", "y"], lat),
        "time": pd.date_range("2014-09-06", periods=3),
        "new": new_axis,
        "reference_time": pd.Timestamp("2014-09-05"),
    },
)

atoms = range(5000)
cells = range(10)
n3 = range(3)

df = f.df
data = df.set_index(['cell','n']).sort_index()
aaa = data[['x','y','z']].to_xarray()
aaa.coords['new'] = n3
positions = xr.concat([aaa['x'], aaa['y'], aaa['z']], aaa.coords['new'])

aaa = data[['i','j','k']].to_xarray()
aaa.coords['new'] = n3
indicies = xr.concat([aaa['i'], aaa['j'], aaa['k']], aaa.coords['new'])


labels = data[['atom']].to_xarray()


ds = xr.Dataset(
    {
        "position" : (['n3', 'cell', 'atoms'], positions),
        "index"    : (['n3', 'cell', 'atoms'], indicies),
        "labels"   : (['cell', 'atoms'], labels)
    },
    coords={
        "atoms": atoms,
        "n3" : n3,
        "cell" : cells,
    },
)
"""



