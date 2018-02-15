import sys
import csv
import numpy as np
import pandas as pd
from itertools import islice

"""
Designed to track crest, foot, and dwend points of dunes from 120122AA time
lapse footage, where dunes are seen in profile and there is no scale known.
Data is input in a .csv file with three lines per dune in a step. Dune class
is borrowed from Kelly's code.
- MY 2/8/2018
"""

fname = 'E:/Boulder_Snow/Tracker/170122AA_Points/170122AA_test.csv'


class Dune:
    """
    This is a class which holds information about a snow dune.
    Each dune is described by three points: one on the crest, one on the foot,
    and one on the dwend.
    These points are defined for each point in time as the dune moves
    across Niwot Ridge.

    To use:
    #Create a dune:
    >> new_dune = Dune(name)
    # Put points in the dune using command
    >> new_dune.add_position(step, (x1,y1), (x2,y2), (x3,y3))
    # Collect points into dataframe
    >> new_dune.finalize()
    # Do some analysis,
    #  e.g. plot position of dune crest against step number:
    >> plt.plot(new_dune['Step'], new_dune['Top'])
    """
    def __init__(self, name):
        """
        This function lists all the properties that a snow dune should have.
        Every python class needs an __init__ function.
        Call this as:
        $new_dune = Dune(name)
        """

        # Give every dune a name. Useful for reference.
        self.name = name

        # Create an empty data frame - this will be a time series
        # containing the dune's position at several points in time.
        self.position = pd.DataFrame

        # Create lists to hold places where the dune is
        self.step = []
        # The dune has three positions: crest, foot, dwend
        # each position is an (x,y) couplet
        self.crest = []
        self.foot = []
        self.dwend = []

    def add_position(self, step, crest, foot, dwend):
        """This function adds a dune position in a step of the video.
        Crest, foot and dwend are (x,y) tuples representing position.
        Step is an integer.
        """
        self.step.append(step)
        self.crest.append(crest)
        self.foot.append(foot)
        self.dwend.append(dwend)

    def finalize_positions(self):
        """Once all positions have been added, collect them in a
        time series (dataframe) structure for easy analysis."""
        self.position['Step'] = pd.Series(self.step)
        self.position['Crest'] = pd.Series(self.crest)
        self.position['Foot'] = pd.Series(self.foot)
        self.position['Dwend'] = pd.Series(self.dwend)
        # Sort the series by step number
        self.position = self.position.set_index('Step')
        self.position = self.sort_index()
        # Empty the lists
        # (So this function can be repeated with no duplication)
        self.step = []
        self.crest = []
        self.foot = []
        self.dwend = []


def find_points(group):
    """Finds the dwend, crest, and foot points of a group of three lines from
    the input csv. Returns a list of tuples in the order dwend, crest, foot."""
    line0 = group[0]
    line1 = group[1]
    line2 = group[2]
    # Pull the points
    p0 = (float(line0[2]), float(line0[3]))
    p1 = (float(line1[2]), float(line1[3]))
    p2 = (float(line2[2]), float(line2[3]))
    pts = [p0, p1, p2]
    xi = [pts[0][0], pts[1][0], pts[2][0]]
    minx = np.where(xi == np.min(xi))[0][0]
    dwend = pts.pop(minx)
    yi = [pts[0][1], pts[1][1]]
    maxy = np.where(yi == np.max(yi))[0][0]
    crest = pts.pop(maxy)
    foot = pts.pop()
    return (crest, foot, dwend)


def add_and_finalize(dunes, name, step, crest, foot, dwend):
    if name in dunes.keys():
        # Add points and finalize
        target_dune = dunes.name
        target_dune.add_position(step, crest, foot, dwend)
        target_dune.finalize_positions()
        dunes[name] = target_dune
    else:
        # Make a new dune, add point, and finalize
        new_dune = Dune(name)
        new_dune.add_position(step, crest, foot, dwend)
        new_dune.finalize_positions()
        dunes[name] = new_dune
    return dunes


def clear_group(group, current):
    group = []
    group.append(current)
    name = current[1]
    step = current[0]
    return (group, name, step)


def read_data(fname):
    """ Read the csv file with all the dune point data"""
    # 1. Open and read the file
    with open(fname, 'r') as datafile:
        # 0. Set up the empty data structure to be filled
        dunes = dict()
        group = []
        name = 'Start'
        step = -1
        datareader = csv.reader(datafile, dialect='excel')
        for line in islice(datareader, 1, None):
            current = line[:]
            cname = current[1]
            cstep = current[0]
            if (name == cname) and (step == cstep):
                group.append(current)
            else:   # 2. For each set of three lines, pull dwend, crest and foot points
                if len(group) == 3:
                    (crest, foot, dwend) = find_points(group)
                    # 3. Assign points to appropriate dune and time
                    dunes = add_and_finalize(dunes, name, step, crest, foot, dwend)
                else:
                    # Print something about how many lines and what dune/time
                    print('Irregular dune {} at step {} has {} lines.'.format(name, step, len(group)))
                # Clear group, add current, and update name and step
                (group, name, step) = clear_group(group, current)
        if len(group) == 3:     # Check end-of-loop group
            (crest, foot, dwend) = find_points(group)
            dunes = add_and_finalize(dunes, name, step, crest, foot, dwend)
        return dunes


# 4. Get heights, widths, slopes, velocities, etc.
# 5. Adjust for perspective
# 6. Check for scaling laws

def main(fname):
    dunes = read_data(fname)
    # Do other things with data analysis

