import matplotlib.pyplot as plt
import numpy as np
import os
from rdp import rdp
import pandas as pd

def angle(dir):
    """
    Returns the angles between vectors.

    Parameters:
    dir is a 2D-array of shape (N,M) representing N vectors in M-dimensional space.

    The return value is a 1D-array of values of shape (N-1,), with each value
    between 0 and pi.

    0 implies the vectors point in the same direction
    pi/2 implies the vectors are orthogonal
    pi implies the vectors point in opposite directions
    """
    dir2 = dir[1:]
    dir1 = dir[:-1]
    return np.arccos((dir1*dir2).sum(axis=1)/(
        np.sqrt((dir1**2).sum(axis=1)*(dir2**2).sum(axis=1))))

"""tolerance = 70
min_angle = np.pi*0.22
df_all = pd.read_csv("/home/reda/Documents/Million/all_players_process.csv",header=None)
df_ball =df_all.iloc[4:150,-5:-3]
df_ball[112] = df_ball[112].astype(float)
df_ball[111] = df_ball[111].astype(float)
points =df_ball[[111,112]].to_numpy()"""


# Use the Ramer-Douglas-Peucker algorithm to simplify the path
# http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
# Python implementation: https://github.com/sebleier/RDP/

def get_turning_point(points, tolerance,min_angle):
    simplified = np.array(rdp(points, tolerance))
    sx, sy = simplified.T
    # compute the direction vectors on the simplified curve
    directions = np.diff(simplified, axis=0)
    theta = angle(directions)
    # Select the index of the points with the greatest theta
    # Large theta is associated with greatest change in direction.
    idx = np.where(theta>min_angle)[0]+1
    return idx, sx, sy

"""
x, y = points.T
fig = plt.figure()
ax =fig.add_subplot(111)

ax.plot(x, y, 'b-', label='original path')
ax.plot(sx, sy, 'g--', label='simplified path')
ax.plot(sx[idx], sy[idx], 'ro', markersize = 10, label='turning points')
ax.invert_yaxis()
plt.legend(loc='best')
plt.show()"""