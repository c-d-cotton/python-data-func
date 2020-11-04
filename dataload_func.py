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

def deletemissinglines_csv(savename, newname = None, replace = False, minlines = 20, sectionchoice = None):
    """
    For a file which is in csv format but has additional headers/footnotes with white lines separating these headers/footnotes from the main block of text. Could also work in other contexts I guess.

    sectionchoice is an integer or None. If 0/1/2/-1 then I would take the first, second, third, last of the white line separated sections in the csv file.
    If sectionchoice is None then take the first section at least minlines lines long.

    If replace is True then set newname = savename.
    """

    if replace is True:
        newname = savename

    with open(savename) as f:
        text = f.read()

    lines = text.split('\n')

    # break up lines into white line separated sections
    sections = []
    section = []
    for line in lines:
        if line == '':
            sections.append(section)
            section = []
        else:
            section.append(line)
    if section != []:
        sections.append(section)

    # decide which section to use
    if sectionchoice is not None:
        mysection = sections[sectionchoice]
    else:
        mysection = None
        for section in sections:
            if len(section) >= minlines:
                mysection = section
                break
        if mysection is None:
            raise ValueError('No sections had a longer length than minlines.')

    with open(newname, 'w+') as f:
        f.write('\n'.join(mysection) + '\n')
