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

def getpanellistfromdatalist(theid, time, datalist):
    """
    Return csv of form timevars,idvars,data.
    time is list of time vars.
    theid is list of id vars.
    datalist is list of data vars.
    datalist is nonempty
    Length of data is length of theid
    Length of each data list is length of time
    """

    if len(theid) > 0:
        if len(time) > 0:
            lentime = time[0]
        else:
            lentime = len(datalist[0]) / len(theid[0])

    theid2 = [t * lentime for t in theid]

    if len(time) > 0:
        if len(theid) > 0:
            lentheid = theid[0]
        else:
            lentheid = len(datalist[0]) / len(time[0])

    time2 = [t * lentheid for t in time]

    return(time2 + theid2 + datalist)


def getcsvfromdatalist(filename, theid, time, datalist, divider=' '):
    thelist = getpanellistfromdatalist(theid, time, datalist)
    curlines = []
    for j in range(0, len(thelist[0])):
        splitline = []

        for i in range(0, len(thelist)):
            splitline.append(i)

        curlines.append(divider.join(splitline))

    with open(filename, 'w+') as f:
        f.write('\n'.join(curlines))
