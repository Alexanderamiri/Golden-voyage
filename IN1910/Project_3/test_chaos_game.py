import numpy as np
from chaos_game import ChaosGame


def test_generate_ngon():
    """
    Test to verify that each side of the polygon has the same length
    """
    polygon = ChaosGame(3, 0.5)
    vec1 = polygon.corner[0]-polygon.corner[1]
    vec2 = polygon.corner[1] - polygon.corner[2]
    sidelength1 = np.sqrt(vec1[0]**2+vec1[1]**2)
    sidelength2 = np.sqrt(vec2[0]**2+vec2[1]**2)
    diff = abs(sidelength1-sidelength2)
    bool = diff < 1e-4
    msg = "The generated polygon does not have equal length sides. " \
          "The sides differ by : {}".format(diff)
    assert bool, msg


def test_number_of_vertices():
    """
    Test to verify that the class produces the right number of vertices
    """
    polygon = ChaosGame(4, 0.5)
    number_of_corners = len(polygon.corner)
    bool = number_of_corners == 4
    msg = "The polygon does not have 3 vertices it has : {}".format(
        number_of_corners)
    assert bool, msg


def test_iterate():
    """
    Test to verify that the class iterates the right number of time
    """
    polygon = ChaosGame()
    polygon.iterate(300)
    length = len(polygon._x)
    bool = length == 300
    msg = "The number of points generated was not 3000, it was : {}".format(
        length)
    assert bool, msg


def test_indices():
    """
    Test to verify that the class produces the right amount of indices
    """
    polygon = ChaosGame(5, 0.5)
    polygon.iterate(500)
    check = any(polygon._indices >= 5)
    msg = "1 or more polygon indices was larger than 5-1"
    assert not check, msg


if __name__ == "__main__":
    test_generate_ngon()
    test_number_of_vertices()
    test_iterate()
    test_indices()
