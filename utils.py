__author__ = 'Nathan.Woodrow'

from qgis.core import QgsPoint

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

def nextvertex(reference_point, distance, angle, virtical_anagle=90):
    """
    Return the next vertex given a start, angle, distance.
    :param reference_point: Start point
    :param distance: Distance to the next vertex
    :param angle: Angle is assumed to already include north correction
    :param virtical_anagle: Virtical angle for height correction
    :return: A tuple of x,y,z for the next point.
    """
    angle = radians(angle)
    virtical_anagle = radians(virtical_anagle)
    d1 = distance * sin(virtical_anagle)
    x = reference_point[0] + d1 * sin(angle)
    y = reference_point[1] + d1 * cos(angle)
    z = reference_point[2] + distance * cos(virtical_anagle)
    return [x, y, z]

def central_angle(chord, radius):
    """
    Central angle given the chord length and radius
    :param chord: Chord length
    :param radius: Radius
    :return: Angle of the central angle from the circle
    """
    angle = chord / float(2 * radius)
    rad = 2 * math.asin(angle)
    return math.degrees(rad)

def arc_length(radius, c_angle):
    """
    The length of the total arc given the radius and central angle.
    :param radius: Radius
    :param c_angle: Central angle of the circle
    :return: The length of the arc
    """
    return 2 * math.pi * radius * ( c_angle / 360 )

def angle_to_center_point(start_anglge, half_cord, radius):
    """
    Angle from chord and radius length.  start_angle will be added to the result for offset
    :param half_cord: The length of the half chord
    :param radius: Radius
    :return: A tuple of (start + angle, angle)
    """
    angle = math.acos(half_cord / float(radius))
    angle = math.degrees(angle)
    return start_anglge + angle, angle

def next_arc_point(angle, opposite, adjacent):



