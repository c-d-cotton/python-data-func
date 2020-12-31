#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

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
