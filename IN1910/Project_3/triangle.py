import numpy as np
import matplotlib.pyplot as plt


def triangle(corner1, corner2):
    """Returns the corners of a equilateral triangle

    Compute the third angle by doing a 60 degree rotation of the vector c2-c1
    and adding it to the first corner c1

    Parameters
    ----------
    corner1 : list
        First corner of the triangle
    corner2 : list
        second corner of the triangle
    Returns
    -------
    list
        list of numpy.array of each corner of the triangle

    """
    corner1 = np.array(corner1)
    corner2 = np.array(corner2)
    vec = corner2-corner1
    d = np.pi/3
    corner3 = np.array([vec[0]*np.cos(d)-vec[1]*np.sin(d)+corner1[0],
                        vec[0]*np.sin(d)+vec[1]*np.cos(d)+corner1[1]])
    return [corner1, corner2, corner3]


def weights(n):
    """Computes n random numbers with sum of 1

    Parameters
    ----------
    n : int
        Number of random numbers that will have a sum of 1
    Returns
    -------
    List
        a list of random numbers with sum of 1

    """
    r = [np.random.random() for _ in range(n)]
    r = [i/sum(r) for i in r]
    return r


def random_starting_point(t):
    """Find 1 random start point within a triangle

    Computes using weights() 1 random starting point

    Parameters
    ----------
    t : list
        Triangle to find a starting point within

    Returns
    -------
    list
        returns 1 randomly computed starting point within the triangle

    """
    r = weights(len(t))
    point = sum([r[i]*t[i] for i in range(len(t))])
    return point


def iterate_ngon(t):
    """Iterates through an n-gon to find new points

    Parameters
    ----------
    t : list
        n-gon

    Returns
    -------
    list
        Sequence of points within n-gon

    """
    x5 = np.zeros((5, 2))
    x5[0] = random_starting_point(t)
    for i in range(4):
        x5[i+1] = (x5[i]+t[np.random.randint(len(t))])*0.5
    points = np.zeros((10000, 2))
    points[0] = x5[-1]
    for i in range(10000-1):
        points[i+1] = (points[i]+t[np.random.randint(len(t))])*0.5
    return points


def iterate_color(t):
    """Iterates through an n-gon to find new points also storing the corner
    used to find the new point

    Parameters
    ----------
    t : list
        n-gon

    Returns
    -------
    list
        list of points within n-gon, list of indices of which corner was used

    """
    number_of_points = 10000
    x5 = np.zeros((5, 2))
    x5[0] = random_starting_point(t)
    for i in range(4):
        x5[i+1] = (x5[i]+t[np.random.randint(len(t))])*0.5
    points = np.zeros((number_of_points, 2))
    indices = np.zeros(number_of_points)
    points[0] = x5[-1]
    for i in range(number_of_points-1):
        indices[i] = np.random.randint(len(t))
        points[i+1] = (points[i]+t[int(indices[i])])*0.5
    return points, indices


def iterate_color_gradient(t):
    """Iterates through an n-gon to find new points as well as making a gradient
    grid for all the points.

    Parameters
    ----------
    t : list
        n-gon

    Returns
    -------
    list
        list of points within n-gon, list of gradient vectors for each point
    """
    number_of_points = 10000
    x5 = np.zeros((5, 2))
    x5[0] = random_starting_point(t)
    for i in range(4):
        x5[i+1] = (x5[i]+t[np.random.randint(len(t))])*0.5
    points = np.zeros((number_of_points, 2))
    points[0] = x5[-1]
    r = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    c = np.zeros((number_of_points, 3))
    indices = np.zeros(number_of_points)
    for i in range(number_of_points-1):
        indices[i] = np.random.randint(len(t))
        c[i+1] = (c[i]+r[int(indices[i])])*0.5
        points[i+1] = (points[i]+t[int(indices[i])])*0.5
    return points, c


if __name__ == '__main__':
    c1 = [0, 0]
    c2 = [1, 0]
    tri = triangle(c1, c2)
    x, colors = iterate_color_gradient(tri)
    fig = plt.figure(dpi=500)
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(*zip(*x), c=colors, s=0.1, marker='.')
    ax.axis('equal')
    plt.show()
