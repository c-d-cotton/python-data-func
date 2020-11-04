#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

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
