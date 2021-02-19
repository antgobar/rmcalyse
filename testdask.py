import dask.dataframe as dd
import pandas as pd

import glob
filelist = glob.glob('/scratch/rmcalyse/rmcalyse/read_in/many/*.rmc6f')

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

