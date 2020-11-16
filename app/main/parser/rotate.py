# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
import numpy as np


def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)


points=[(200, 300), (100, 300)]
origin=(100,100)

new_points = rotate(points, origin=origin, degrees=10)
print(new_points)