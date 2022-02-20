#!/usr/bin/env python3

from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt
import math

# Wheelbase [meter]
WB = 2.0
# Time interval [sec]
DT = 0.1

class VehicleState:
    def __init__(self, x, y, yaw, v=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.calc_front_wheel_position()

    def calc_front_wheel_position(self):
        self.front_x = self.x + WB * math.cos(self.yaw)
        self.front_y = self.y + WB * math.sin(self.yaw)

    def update(self, acc, steer_angle):
        self.v += acc * DT
        self.yaw += self.v * DT * math.sin(steer_angle) / WB
        self.x += self.v * DT * math.cos(self.yaw)
        self.y += self.v * DT * math.sin(self.yaw)
        self.calc_front_wheel_position()


def simple_lateral_control(vehicle_state, course_x, course_y):
    # Calc nearest point
    nearest_index = 0
    nearest_dist = np.inf
    for i, (cx, cy) in enumerate(zip(course_x, course_y)):
        dist = (vehicle_state.x - cx)**2 + (vehicle_state.y - cy)**2
        if dist < nearest_dist:
            nearest_index = i
            nearest_dist = dist

    return (course_y[nearest_index] - vehicle_state.y)


def generate_spline_course(ref_x: list[float], ref_y: list[float], points_num: int):
    assert(len(ref_x) == len(ref_y))
    assert(len(ref_x) > 1)

    x = np.linspace(np.min(ref_x), np.max(ref_x), num=points_num)
    y = CubicSpline(ref_x, ref_y)(x)

    return x, y


if __name__ == '__main__':

    vs = VehicleState(0., 1., 0., 3.0)

    reference_points_x = [0., 10., 20., 30.]
    reference_points_y = [1., 1., 2., -1.]

    course_x, course_y = generate_spline_course(reference_points_x, reference_points_y, 100)
    trajectory_x, trajectory_y = [vs.x], [vs.y]

    while vs.x <= np.max(course_x):
        acc = 0.0
        steer = simple_lateral_control(vs, course_x, course_y)
        vs.update(acc, steer)
        trajectory_x.append(vs.x)
        trajectory_y.append(vs.y)
        #plt.arrow(vs.x, vs.y, 0.1*math.cos(vs.yaw), 0.1*math.sin(vs.yaw))


    plt.plot(course_x, course_y, color='blue', label='target course')
    plt.plot(trajectory_x, trajectory_y, color='green', label='vehicle trajectory')

    plt.legend(loc='upper left')
    plt.xlabel('x')
    plt.xlabel('y')
    plt.show()
