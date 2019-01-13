__author__ = "Nathan.Woodrow"

import unittest
import math

from matplotlib import pyplot
from utils import nextvertex, arc_points, calculate_center, calculate_midpoint, Point
from collections import namedtuple


class MyTestCase(unittest.TestCase):
    def test_longestlength(self):
        points = []
        angle = 45
        distance = 10
        radius = distance

        start = Point(float(5), float(5))
        end = nextvertex(start, distance, angle)

        center = calculate_center(start, end, radius, distance)

        print(start)
        print(end)
        print(center)

        points.append(start)
        points.append(end)
        line_points = []
        line_points.append(start)
        line_points.append(end)
        arcpoints_clock = list(arc_points(start, end, distance, radius, 20))
        arcpoints_anti = list(
            arc_points(start, end, distance, radius, 20, direction="anit")
        )
        pyplot.plot(*zip(*points), marker="o", color="r", ls="")
        pyplot.plot(*zip(*arcpoints_anti), marker="o", color="y", ls="")
        pyplot.plot(*zip(*arcpoints_clock), marker="o", color="b", ls="")
        pyplot.plot(*zip(*line_points))
        c2 = pyplot.Circle(center, radius, color="0.75")
        fig = pyplot.gcf()
        fig.gca().add_artist(c2)
        pyplot.axis([0, 30, 0, 30])
        pyplot.show()

        # def test_angle_to_center(self):
        # start_angle = 30
        # half_chord = 5
        #     radius = 20
        #     angle = angle_to_center_point(0, half_chord, radius)
        #     print "Angle", angle

        # def test_longestlength(self):
        #     length_1 = 10
        #     length_2 = 5
        #     a=[[3,2],[7,4]]
        #     angle = angle_to_center_point(0, 5, 20)
        #     print angle
        #     centerpoint = nextvertex([3,2, 0], length_1, angle)
        #     a.append([centerpoint[0], centerpoint[1]])
        #     pyplot.plot(*zip(*a), marker='o', color='r', ls='')
        #     pyplot.show()
        #     print "Distnace", distance_to_point(length_1, length_2)


if __name__ == "__main__":
    unittest.main()
