__author__ = 'Nathan.Woodrow'

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

