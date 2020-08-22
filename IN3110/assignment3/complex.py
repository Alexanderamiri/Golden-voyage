from numpy import sqrt


class Complex:
    def __init__(self, a, b):
        self.real = a
        self.imag = b

    # Assignment 3.3

    def __str__(self):
        if self.imag >= 0:
            return "{}+{}i".format(self.real, self.imag)
        else:
            return "{}{}i".format(self.real, self.imag)

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def modulus(self):
        return sqrt(self.real ** 2 + self.imag ** 2)

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Complex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __eq__(self, other):
        return (self.real == other.real) and (self.imag == other.imag)

    # Assignment 3.4
    def __radd__(self, other):
        return self.__add__(Complex(other.real, other.imag))

    def __rmul__(self, other):
        return self.__mul__(Complex(other.real, other.imag))

    def __rsub__(self, other):
        return self.__sub__(Complex(other.real, other.imag))

    # Optional, possibly useful methods

    # Allows you to write `-a`

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    # Make the `complex` function turn this into Python's version of
    # a complex number
    def __complex__(self):
        return complex("{:f}+{:f}j".format(self.real, self.imag))
