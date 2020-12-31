#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import pandas as pd

def loadfred(csvpath, frequency, varname = None, dropdate = True, timevar = True):
    """
    Frequency should be one of 'Y', 'Q', 'M'
    Should be saved as a csv
    """
    df = pd.read_csv(csvpath)

    if varname is not None:
        df = df.rename(columns = {df.columns[1]: varname})

    if frequency == 'Y':
        year = [int(date[0: 4]) for date in df['DATE']]
        if timevar is True:
            df['time'] = year
        else:
            df['year'] = year
    elif frequency == 'Q':
        year = [int(date[0: 4]) for date in df['DATE']]
        quarter = [int(date[5: 7]) // 3 + 1 for date in df['DATE']]
        if timevar is True:
            df['time'] = [year[i] * 4 + quarter[i] - 1 for i in range(len(year))]
        else:
            df['year'] = year
            df['quarter'] = quarter
    elif frequency == 'M':
        year = [int(date[0: 4]) for date in df['DATE']]
        month = [int(date[5: 7]) for date in df['DATE']]
        if timevar is True:
            df['time'] = [year[i] * 12 + month[i] - 1 for i in range(len(year))]
        else:
            df['year'] = year
            df['month'] = month
    else:
        raise ValueError('frequency misspecified')

    if dropdate is True:
        df = df.drop('DATE', axis = 1)

    return(df)
