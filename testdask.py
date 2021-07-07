import dask.dataframe as dd
import pandas as pd

import glob

from rmcalyse.log_setup import add_logging_handlers
from rmcalyse.framework import Framework

f = Framework.from_yaml('rmcalyse/input.yaml')



"""filelist = glob.glob('/scratch/rmcalyse/rmcalyse/read_in/many/*.rmc6f')

def strip_brackets(s):
    try:
        return int(s[1:-1])
    except:
        return s

def rmc6f_to_df(filepath):
    with open(filepath,'r') as f:
        meta = []
        for line in f:
            if line != 'Atoms:\n':
                meta.append(line.replace( '\n' , ''))
            else:
                break
    df = dd.read_csv(filepath,skiprows=len(meta)+1,header=None, delim_whitespace=True, names = ['n','atom','label','x','y','z','original','i','j','k'], converters={'label':strip_brackets})
    return meta, df

for i,f in enumerate(filelist):
    if i == 0:
        m,df = rmc6f_to_df(f)
        df['cell'] = i
    else:
        m,tmp = rmc6f_to_df(f)
        tmp['cell'] = i
        df = df.append(tmp)
df = df.categorize(columns=['atom', 'cell'])

# we now has a df with 50000 rows in

#can save it with dd.to_parquet(df, 'parquet.parquet')
# aqnd load with df = dd.read_parquet('parquet.parquet')




# so how will this work? 

# 1. read the yaml file to identify the plugin chain requested
# 2. use the plugin factory to instantiate the plugin objects
#      ** if a function only does delayed work it is very fast **
# 3. ...so we run the plugins using the process method



def test_dask_function(df, number):
    df['what'] = number
    return df

dddf = df[['x','y','z']]
anarray = dddf.to_dask_array(lengths=True)

# HACK TODO
cell = [39.3399, 39.3399, 39.3399, 90.0, 90.0, 90.0]
import numpy as np
a,b,c = cell[:3]

al,be,ga = np.deg2rad(cell[3:])
V = a*b*c * (1 - np.cos(al)**2 - np.cos(be)**2 -np.cos(ga)**2 + 2*np.cos(al)*np.cos(be)*np.cos(ga))**0.5
a1 = a
a2 = 0
a3 = 0
b1 = b * np.cos(ga)
b2 = b * np.sin(ga)
b3 = 0
c1 = c * np.cos(be)
c2 = c * (np.cos(al) - (np.cos(be) * np.cos(ga))) / np.sin(ga)
c3 = V / (a * b * np.sin(ga))
M = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])

something = M @ anarray.T

print("I made...  something?")

# plugin gets given a df
# plugin knows what columns it wants to extract
# plugin calls inherited method (probably) to get dask.array of required columns

from rmcalyse.core.readyaml import load_yaml
c = load_yaml('rmcalyse/input.yaml')

print('c is a linted config')


so something like...

1. rmcalyse.go my_config.yaml
    the cli instantiates a runner object and lints the yaml file
    the runner then proceeds to instantiate the plugins one by one, and the process method is called with the metadata and path to the df as an argument
        - shuold these be delayed in some way?
    a plug which just requires metadata and df is fine
        - how does a plugin requiring a new input get what it needs?
    the runner calls compute at the end




"""

