__author__ = 'Nathan.Woodrow'

import math
from qgis.core import QgsPoint, QgsFeature, QgsGeometry, QgsMessageLog
from collections import namedtuple


def azimuth_from_line(geometry):
    line = geometry.asPolyline()
    p1 = line[0]
    p2 = line[1]
    az = p1.azimuth(p2)
    return az


def createpoints(points):
    for point in points:
        geom = QgsGeometry.fromPoint(point)
        feature = QgsFeature()
        feature.setGeometry(geom)
        yield feature


def createline(points):
    """
    Creata a line feature from a list of points
    :param points: List of QgsPoints
    """
    geom = QgsGeometry.fromPolyline(points)
    feature = QgsFeature()
    feature.setGeometry(geom)
    return feature


def createpolygon(polygon):
    """
    Create a polygon from a list of points
    :param points: List of QgsPoints
    """
    geom = QgsGeometry.fromPolygon(polygon)
    if not geom:
        return None
    feature = QgsFeature()
    feature.setGeometry(geom)
    return feature

class Point(QgsPoint):
    def __init__(self, x, y, z=0, arc_point=False):
        QgsPoint.__init__(self, x, y)
        self.arc_point = arc_point
        self.z = z

    @property
    def x(self):
        return QgsPoint.x(self)

    @property
    def y(self):
        return QgsPoint.y(self)

def to_qgspoints(points, repeatfirst=False):
    """
    Generate a QgsPoint list from a list of x,y pairs
    :param repeatfirst: Repeat the first item in the list for each other point
    :return:
    """
    if not repeatfirst:
        # Just return a full list like normal
        return [QgsPoint(point[0], point[1]) for point in points]
    else:
        pointlist = []

        # Pop the first point
        points = iter(points)
        v0 = points.next()
        v0 = QgsPoint(v0[0], v0[1])

        # Loop the rest
        for point in points:
            p = QgsPoint(point[0], point[1])
            pointlist.append(v0)
            pointlist.append(p)
        return pointlist


def pairs(points, matchtail):
    """
    Return a list of pairs from a list of points
    :param matchtail: The HEAD of the next pair will be the TAIL of the current pair e.g pair[1] == next[0]
    :param points: List of points to process
    :return:
    """
    if matchtail:
        it = zip(points, points[1:])
    else:
        it = zip(points[::2], points[1::2])

    for start, end in it:
        yield [start, end]


def nextvertex(reference_point, distance, angle, zenith_angle=0, arc_point=False):
    """
    Return the next vertex given a start, angle, distance.
    :param reference_point: Start point
    :param distance: Distance to the next vertex
    :param angle: Angle is assumed to already include north correction
    :param zenith_angle: Zenith angle for height correction
    :return: A tuple of x,y,z for the next point.
    """
    angle = math.radians(angle)
    zenith_angle = math.radians(zenith_angle)
    d1 = distance * math.sin(zenith_angle)
    x = reference_point.x + d1 * math.sin(angle)
    y = reference_point.y + d1 * math.cos(angle)
    z = reference_point.z + distance * math.cos(zenith_angle)
    return Point(x, y, z, arc_point)


def arc_length(radius, c_angle):
    """
    The length of the total arc given the radius and central angle.
    :param radius: Radius
    :param c_angle: Central angle of the circle
    :return: The length of the arc
    """
    return 2 * math.pi * radius * ( c_angle / 360 )


def points_on_arc(count, center, radius, start, end):
    pass

def dmsToDd(dms):
    "It's not fast, but it's a safe way of dealing with DMS"
    #dms=dms.replace(" ", "")
    if isinstance(dms, float):
        return dms
    for c in dms:
        if ((not c.isdigit()) and (c != '.') and (c != '-')):
            dms=dms.replace(c,';')
    while (dms.find(";;")>=0):
        dms=dms.replace(";;",';')
    if dms[0]==';':
        dms=dms[1:]
    dms=dms.split(";")
    dd=0
    #dd=str(float(dms[0])+float(dms[1])/60+float(dms[2])/3600)
    for row, f in enumerate(dms):
        if f!="":
            dd+=float(f)/pow(60, row)
    return dd

def gradianToDd(gradian):
    factor = 1
    out = ''
    for c in gradian:
        if c in 'cC':
            factor *= 0.01
        if c.isdigit() or c in '.-':
            out += c
    return float(out) * factor * 0.9

def angle_to(p1, p2):
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    rads = math.atan2(xDiff, yDiff)
    angle = math.degrees(rads)
    if angle < 0:
        angle += 360
    return angle


def calculate_center(start, end, radius, distance):
    def func(diff):
        half = distance / 2
        return math.sqrt(radius ** 2 - half ** 2) * diff / distance

    midpoint = calculate_midpoint(start, end)
    return Point(midpoint.x - func(start.y - end.y), midpoint.y - func(end.x - start.x))


def calculate_midpoint(start, end):
    midpoint = Point((start.x + end.x) / 2, (start.y + end.y) / 2)
    return midpoint

class Direction:
    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    @classmethod
    def resolve(cls, value):
        if value == 'a' or value == "anticlockwise":
            return Direction.ANTICLOCKWISE
        else:
            return Direction.CLOCKWISE


def arc_points(start, end, distance, radius, point_count=20, direction=Direction.CLOCKWISE):
    center = calculate_center(start, end, radius, distance)

    first_angle = angle_to(start, center)
    last_angle = angle_to(end, center)
    if direction == Direction.ANTICLOCKWISE:
        last_angle, first_angle = first_angle, last_angle

    if first_angle < last_angle:
        sweep = last_angle - first_angle
    elif first_angle > last_angle:
        last_angle += 360
        sweep = last_angle - first_angle
    else:
        sweep = 0

    alpha = sweep / float(point_count)
    if sweep < 0:
        alpha *= -1.0

    print "First:", first_angle
    print "Last:", last_angle
    print "Sweep", sweep
    print "Alpha", alpha

    a = first_angle
    for i in range(point_count + 1):
        a += alpha
        if not a >= last_angle and not a <= first_angle:
            yield nextvertex(center, radius, a, arc_point=True)


