#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import numpy as np
import pandas as pd

# No Gaps Time Variable:{{{1
def dfwithoutgaps_time(df, timevar, groupbyterms = None,  merge = False, merge_deleteindicator = True):
    """
    Create a dataset with no missing gaps for the timevar

    If merge is True then merge back into main df dataframe
    If merge_deleteindicator is True then when merge, leave indicator for whether the variable is temporary or not
    """
    import itertools

    if groupbyterms is None:
        groupbyterms = []
    if isinstance(groupbyterms, str):
        groupbyterms = [groupbyterms]

    mintime = int(np.min(df[timevar]))
    maxtime = int(np.max(df[timevar]))
    times = list(range(mintime, maxtime + 1))

    listofuniquegroupbyterms = []
    for group in groupbyterms:
        listofuniquegroupbyterms.append(list(set(df[group])))

    list1 = list(itertools.product(*listofuniquegroupbyterms, times))
    dftime = pd.DataFrame(list1, columns = groupbyterms + [timevar])

    if merge is True:

        timevarindicator = '__temp__time__var__indicator__'
        if timevarindicator in df.columns or timevarindicator + '_time' in df.columns:
            raise ValueError('Temporary time variable indicator already exists in df.')

        # add timevarindicator to each dataset to help indicate whether a row comes from original df or I added it
        df[timevarindicator] = 0
        dftime[timevarindicator] = 1

        df = df.merge(dftime, on = groupbyterms + [timevar], suffixes = ('', '_time'), how = 'outer')
        df[timevarindicator].fillna(df[timevarindicator + '_time'], inplace = True)
        del df[timevarindicator + '_time']

        df = df.sort_values(groupbyterms + [timevar])

        if merge_deleteindicator is True:
            df = df.drop(timevarindicator, axis = 1)

        return(df)

    else:
        return(dftime)


# Convert Monthly/Quarterly/Yearly:{{{1
def timeaggregate(df, aggregateperiodsize, timevarname = 'time', offset = 0, aggregatetype = 'last', replacetimevar = True):
    """
    If aggregateperiodsize is 4 (quarterly data) then period 0 in the aggregated data covers periods 0: 3 in the original data
    If aggregateperiodsize is 4 (quarterly data) and offset == 0 then period 0 in the aggregated data covers periods 1: 4 in the original data

    If aggregatetype == 'last', take the last period in the original range to be the value of the aggregated data period
    If aggregatetype == 'mean', sum the periods in the original range to be the value of the aggregated data period
    """
    # fill in any gaps
    # not actually necessary if use groupby
    # df = dfwithoutgaps_time(df, timevarname)

    # get the aggregate period time
    df['aggregatedtime'] = (df[timevarname] - offset) // aggregateperiodsize 

    if aggregatetype == 'last':
        df = df.groupby(['aggregatedtime']).last()
    elif aggregatetype == 'mean':
        df = df.groupby(['aggregatedtime']).mean()
    elif aggregatetype == 'first':
        df = df.groupby(['aggregatedtime']).first()
    else:
        raise ValueError('aggregatetype misspecified')



    if replacetimevar is True:
        df = df.drop('time', axis = 1)
        df['time'] = df.index
        df.index.name = ''

    return(df)
    

def timeaggregate_test():
    df = pd.DataFrame({'time': list(range(100)), 'var1': list(range(100))})
    df = timeaggregate(df, 4)
    print(df.head())


# Lag/Forward Functions:{{{1
def addlagsforwards(df, variables, lagforwardnums, lagterm = '_lag', forwardterm = '_forward', groupbyterms = None, concat = False, timevar = None):
    """
    Assumes data already ordered correctly.
    Take named variables from pandas df and add lags/forwards.
    lagforwardnums = [-2, 1] means add lag2 and forward1
    groupbyterms used with panel data i.e. groupbyterms = ['country'] adds lags by country
    concat means add to the initial dataset
    timevar allows me to avoid issues with missing periods i.e. the lag of 2016 will not be correct if I am missing data for 2015 but have data for 2014. timevar needs to be a consecutive integer variable (when no periods are missing)
    """

    if isinstance(variables, str):
        variables = [variables]
    if isinstance(groupbyterms, str):
        groupbyterms = [groupbyterms]

    if timevar is not None:
        df = dfwithoutgaps_time(df, timevar, groupbyterms = groupbyterms,  merge = True)

    df2 = pd.DataFrame(index = df.index)
    for var in variables:
        for lag in lagforwardnums:
            if lag <= 0:
                lagforwardterm = lagterm + str(lag).strip('-')
            else:
                lagforwardterm = forwardterm + str(lag)
            if groupbyterms == None:
                df2[var + lagforwardterm] = df[var].shift(-lag)
            else:
                df2[var + lagforwardterm] = df.groupby(groupbyterms)[var].shift(-lag)
    if concat == True:
        df2 = pd.concat((df, df2), axis = 1)
    return(df2)


def test():

    year1 = [2014, 2015, 2016, 2017]
    type1 = ['a'] * 4
    data1 = [np.nan, 2, 3, 4]
    year2 = [2014, 2016, 2017]
    type2 = ['b'] * 3
    data2 = [1, 3, 4]

    df = pd.DataFrame(data = {'year': year1 + year2})
    df['type'] = type1 + type2
    df['data'] = data1 + data2

    df = addlagsforwards(df, 'data', lagforwardnums = [-2, -1, 1], groupbyterms = 'type', timevar = 'year', concat = True)
    print(df)


# Smoothing Functions:{{{1
def simpleweightedsmooth(df, variables, smoothingcombinations):
    """
    smoothingcombinations = [[-3, 0], [-4, 4]]

    Need to add lags beforehand.
    """
    if isinstance(variables, str):
        variables = [variables]
    if isinstance(smoothingcombinations[0], int):
        smoothingcombinations = [smoothingcombinations]

    for variable in variables:
        for combo in smoothingcombinations:
            varlist = []
            for number in range(combo[0], combo[1] + 1):
                if number < 0:
                    variable2 = variable + '_' + 'lag' + str(abs(number))
                elif number == 0:
                    variable2 = variable
                else:
                    variable2 = variable + '_' + 'forward' + str(number)
                varlist.append(variable2)
            
            if combo[0] < 0:
                pre1 = 'lag'
            elif combo[0] == 0:
                pre1 = ''
            else:
                pre1 = 'forward'
            if combo[1] < 0:
                pre2 = 'lag'
            elif combo[1] == 0:
                pre2 = ''
            else:
                pre2 = 'forward'
            
            df[variable + '_' + pre1 + str(abs(combo[0])) + '_' + pre2 + str(abs(combo[1]))] = df[varlist].mean(axis = 1, skipna = False)

    return(df)

