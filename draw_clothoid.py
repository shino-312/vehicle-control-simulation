#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import copy

class PathPoint:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.curvature = 0.
        self.angle = 0.

def generate_arc(radius, angle):
    t = np.arange(0, angle, 0.01)
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    a = np.pi/2 + t
    temp = PathPoint()
    ret = []
    for xi, yi, ai in zip(x, y, a):
        temp.x = xi
        temp.y = yi
        temp.angle = ai
        temp.curvature = 1./radius
        ret.append(copy.deepcopy(temp))
    return ret

def generate_clothoid(radius):
    t = np.arange(0, 5, 0.01)
    func_x = np.cos(t**2 / 2)
    func_y = np.sin(t**2 / 2)
    curvature = t
    integrate_x = sp.integrate.cumulative_trapezoid(func_x, t, initial=0)
    integrate_y = sp.integrate.cumulative_trapezoid(func_y, t, initial=0)
    temp = PathPoint()
    ret = []
    
    for x, y, c in zip(integrate_x, integrate_y, curvature):
        if c < 1./radius:
            temp.x = x
            temp.y = y
            temp.angle = c / (2.*radius)
            temp.curvature = c
            ret.append(copy.deepcopy(temp))
    return ret

def join_path(path_array):
    ret = []
    for path in path_array:
        print('join_path %d points' %(len(path)))
        if not ret:
            ret = copy.deepcopy(path)
            continue

        last_point = ret[-1]
        diff_x = 0.0 
        diff_y = 0.0 
        diff_angle = 0.0 
        temp = PathPoint()

        for i, point in enumerate(path):
            if i == 0:
                diff_angle =  last_point.angle - point.angle
                temp.x = point.x * np.cos(diff_angle) - point.y * np.sin(diff_angle)
                temp.y = point.x * np.sin(diff_angle) + point.y * np.cos(diff_angle)
                diff_x =  last_point.x - temp.x
                diff_y =  last_point.y - temp.y
                temp.x += diff_x
                temp.y += diff_y
            else:
                temp.x = point.x * np.cos(diff_angle) - point.y * np.sin(diff_angle) + diff_x
                temp.y = point.x * np.sin(diff_angle) + point.y * np.cos(diff_angle) + diff_y

            temp.angle = point.angle + diff_angle
            temp.curvature = point.curvature
            ret.append(copy.deepcopy(temp))
    return ret

def extract_x_y(path_array):
    x = []
    y = []
    for p in path_array:
        x.append(p.x)
        y.append(p.y)
    return x, y

clothoid= generate_clothoid(0.3)
arc = generate_arc(0.3, np.pi*2)

joined_curve = join_path([clothoid, arc])

plot_x, plot_y = extract_x_y(joined_curve)
plt.plot(plot_x, plot_y)
plt.show()
