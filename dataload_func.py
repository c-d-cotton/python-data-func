#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

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
