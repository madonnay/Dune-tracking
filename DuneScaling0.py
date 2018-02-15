# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 16:42:11 2018

@author: yoder
"""

'''Analyze dunes from three given points'''

import sys
import csv
import numpy as np
import pandas as pd
from itertools import islice

fname = 'E:\Boulder_Snow\Tracker\170122AA_Points\170122AA_test.csv'
# 0. Set up the empty data structure to be filled
n = 0   # Number of total dunes
d = dict()   # Dictionary of dune codes and dune numbers

# 1. Open and read the file
with open(fname, 'r') as datafile:
    datareader = csv.reader(datafile, dialect='excel')
    for line in islice(datareader, 1, None, 3):
        # 2. For each set of three lines, pull tail, crest and foot points
        line0 = datareader.next()
        line1 = datareader.next()
        line2 = datareader.next()
        # Check if all three lines are for the same dune
        if line0(1) == line2(1):
            di = line0(1)
            # Check if di is in d and if not, add it and increment n
            if di not in d:
                d[di] = n
                n += 1
        else:
            sys.exit("Data is improperly aligned")
        # Pull the points
        p0 = (float(line0(2)), float(line0(3)))
        p1 = (float(line1(2)), float(line1(3)))
        p2 = (float(line2(2)), float(line2(3)))
        pts = [p0, p1, p2]
        xi = [pts[0][0], pts[1][0], pts[2][0]]
        minx = np.where(xi == np.min(xi))[0][0]
        tail = pts.pop(minx)
        yi = [pts[0][1], pts[1][1]]
        maxy = np.where(yi == np.max(yi))[0][0]
        crest = pts.pop(maxy)
        foot = pts.pop()
        # 3. Assign points to appropriate dune and time
        ti = int(line0(0))
        

# 4. Get heights, widths, slopes, velocities, etc.
# 5. Adjust for perspective
# 6. Check for scaling laws
