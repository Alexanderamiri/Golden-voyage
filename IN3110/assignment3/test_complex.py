from complex import Complex
from numpy import sqrt


def test___add__():
    z1 = Complex(1, 2)
    z2 = Complex(3, 1)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert z1 + z2 == Complex(
        4, 3
    ), "{} + {} was equal to {} and not (" "4+3i)".format(z1, z2, z1 + z2)
    assert z1 + z4 == Complex(
        3, 2
    ), "{} + {} was equal to {} and not (" "3+2i)".format(z1, z2, z3)
    assert z3 + z2 == Complex(
        3, 3
    ), "{} + {} was equal to {} and not (" "5+1i)".format(z3, z2, z3 + z2)


def test___sub__():
    z1 = Complex(1, 2)
    z2 = Complex(3, 1)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert z1 - z2 == Complex(
        -2, 1
    ), "1+2i - 3+1i was equal to {} and" " not -2+1i".format(z1 - z2)
    assert z1 - z4 == Complex(
        -1, 2
    ), "1+2i - 2+0i was equal to {} and not" "-1+2i".format(z1 - z4)
    assert z3 - z2 == Complex(
        -3, 1
    ), "0+2i - 4+1i was equal to {} and not" "-3+1i".format(z3 - z2)


def test_conjugate():
    z1 = Complex(1, 2)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert z1.conjugate() == Complex(1, -2), (
        "Conjugate of {} was equal to {}"
        " and not 1-2i".format(z1, z1.conjugate())
    )
    assert z3.conjugate() == Complex(0, -2), (
        "Conjugate of {} was equal to {} "
        "and not 0-2i".format(z3, z3.conjugate())
    )
    assert z4.conjugate() == Complex(
        2, 0
    ), "Conjugate of {} was equal to {}" " and not 2".format(
        z4, z4.conjugate()
    )


def test_modulus():
    z1 = Complex(1, 2)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert (
        abs(z1.modulus() - sqrt(5)) < 1e-8
    ), " Modulus of {} was equal to {} and not sqrt(5) ".format(
        z1, z1.modulus()
    )
    assert (
        abs(z3.modulus() - sqrt(4)) < 1e-8
    ), "Modulus of {} was equal to {} and not sqrt(2) ".format(
        z3, z3.modulus()
    )
    assert (
        abs(z4.modulus() - sqrt(4)) < 1e-8
    ), " Modulus of {} was equal to {} and not sqrt(2) ".format(
        z4, z4.modulus()
    )


def test___eq__():
    z1 = Complex(1, 2)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert z1 == Complex(
        1, 2
    ), "The complex number 1+2i was equal to {}" " and not 1+2i".format(z1)
    assert z3 == Complex(
        0, 2
    ), "The complex number 1+2i was equal to {} " "and not 2i".format(z1)
    assert z4 == Complex(
        2, 0
    ), "The real number 2 was equal to {}" " and not 2".format(z1)


def test___mul__():
    z1 = Complex(1, 2)
    z2 = Complex(3, 1)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert z1 * z2 == Complex(
        1, 7
    ), "1+2i * 3+1i was equal to {} and not 1+7i".format(z1 * z2)
    assert z1 * z3 == Complex(
        -4, 2
    ), "1+2i * 0+2i was equal to {} and not -4+2i".format(z1 * z3)
    assert z3 * z4 == Complex(
        0, 4
    ), "0+2i * 2+0i was equal to {} and not 4i".format(z3 * z4)


def test___radd__():
    z1 = Complex(1, 2)
    z2 = Complex(2, 3)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert 2 + z3 == Complex(2, 2), "2+2i was not 2+2i "
    assert 2 + z4 == Complex(4, 0), "2+2 was not 4"
    assert (2 + 2j) + z2 == Complex(4, 5), "(2+2j)+(3+1i) was not 5+3i "


def test___rsub__():
    z1 = Complex(1, 2)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert 1 - z1 == Complex(0, 2), "1 - 1+2i was not 0+2i"
    assert 1 - z4 == Complex(1, 0), "1 - 2 was not 1+0i"
    assert 1j - z3 == Complex(0, 1), "1 - 2i was not 1-2i"


def test___rmul__():
    z1 = Complex(1, 2)
    z2 = Complex(3, 1)
    z3 = Complex(0, 2)
    z4 = Complex(2, 0)
    assert 2 * z1 == Complex(2, 4), "2*(1+2i) was not 2+2i "
    assert 2 * z3 == Complex(0, 4), "2*2i was not 0+4i "
    assert 2 * z4 == Complex(4, 0), "2*2 was not 4+0i "
    assert 4 * Complex(3, 4) - 2 == Complex(10, 16)


if __name__ == "__main__":
    test___add__()
    test___eq__()
    test___sub__()
    test_conjugate()
    test_modulus()
    test___mul__()
    test___radd__()
    test___rsub__()
    test___rmul__()
