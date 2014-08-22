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

