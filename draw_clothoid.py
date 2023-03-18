#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

t = np.arange(0, 5, 0.01)
x = np.cos(t**2 / 2)
y = np.sin(t**2 / 2)

integrate_x = sp.integrate.cumulative_trapezoid(x, t, initial=0)
integrate_y = sp.integrate.cumulative_trapezoid(y, t, initial=0)

plt.plot(integrate_x, integrate_y)
plt.show()
