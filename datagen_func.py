#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

def addcategoricalinteraction(df, categorical, variables, concat = False):
    """
    If have categorical usstate and variable rainfall, outputs 50 variables.
    Each variable has zeroes except for one state where has value of rainfall.
    concat appends data to original df. Otherwise, output new df.
    """
    import pandas

    df2 = pandas.DataFrame(index = df.index)
    zerovariable = [0] * len(df.index)
    listcategorical = list(df[categorical])
    for variable in variables:
        listvariable = list(df[variable])
        for category in df[categorical].unique():
            newvariable = zerovariable[:]
            trueval = [i for i in range(len(df.index)) if listcategorical[i] == category]
            for i in trueval:
                newvariable[i] = listvariable[i]
            df2[variable + '_&&_' + category] = newvariable
    return(df2)
        


