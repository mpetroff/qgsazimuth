__author__ = 'Nathan.Woodrow'

import unittest
import math

def central_angle(chord, radius):
    angle = chord / float(2 * radius)
    rad = 2 * math.asin(angle)
    return math.degrees(rad)

def arc_length(radius, c_angle):
    return 2 * math.pi * radius * ( c_angle / 360 )

def angle_to_center_point(half_cord, radius):
    return math.acos(half_cord / float(radius))

def calc_point_count(length, c_angle):
    return int()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        radius = 10
        chord = 10
        angle = central_angle(chord, radius)
        print angle
        print arc_length(radius, c_angle=angle)

    def test_angle_to_center(self):
        start_angle = 30
        half_chord = 5
        radius = 20
        angle = angle_to_center_point(half_chord, radius)
        print angle
        print math.degrees(angle)
        print start_angle + math.degrees(angle)

if __name__ == '__main__':
    unittest.main()
