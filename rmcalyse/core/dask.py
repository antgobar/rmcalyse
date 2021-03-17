import dask.dataframe as dd
import pandas as pd

from rmcalyse.general_functions.read_rmc6f import convert_meta_list_to_meta_object

def strip_brackets(s):
    try:
        return int(s[1:-1])
    except:
        return s

class Cols:
    N = 'n'
    ATOM = 'atom'
    LABEL = 'label'
    X = 'x'
    Y = 'y'
    Z = 'z'
    ORIG = 'original'
    I ='i'
    J = 'j'
    K = 'k'
    CELL = 'cell'

def _load_rmc6f_file(filepath, metalines=False):
    meta = []
    if not metalines:
        with open(filepath,'r') as f:
            for line in f:
                if line != 'Atoms:\n':
                    meta.append(line.replace( '\n' , ''))
                else:
                    break
        metalines = len(meta)
    df = pd.read_csv(
            filepath,
            skiprows = metalines + 1,
            header = None, 
            delim_whitespace = True, 
            names = [Cols.N, Cols.ATOM, Cols.LABEL, Cols.X, Cols.Y, Cols.Z, Cols.ORIG, Cols.I, Cols.J, Cols.K],
            converters = {Cols.LABEL:strip_brackets},
            )
    return df, meta, metalines

def load_rmc6f_files(filelist):
    for i,f in enumerate(filelist):
        if i == 0:
            df, meta, metalines = _load_rmc6f_file(f)
            df[Cols.CELL] = i
        else:
            tmp,_,_ = _load_rmc6f_file(f, metalines)
            tmp[Cols.CELL] = i
            df = df.append(tmp)
    #df = df.categorize(columns=[Cols.ATOM,Cols.CELL])
    meta = convert_meta_list_to_meta_object(meta)
    return df, meta

def load_parquet_file(filename):
    return dd.read_parquet(filename)

def to_parquet_file(df, filename):
    df.to_parquet(filename)

