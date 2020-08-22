import numpy as np
import matplotlib.pyplot as plt


class AffineTransform:
    """
    A class to Affine transforms a set of x and y values using barnsley ferns
    suggestions of variables and probabilities

    Parameters
    ----------
    a, b, c, d, e, f : float
        Numbers used for affine transformation
    """
    def __init__(self, a=0.0, b=0.0, c=0.0, d=0.0, e=0.0, f=0.0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def __call__(self, x, y):
        """
        This call function to produce the affine transformed point

        Parameters
        ----------
        x, y : float
            coordinates of a single point

        Returns
        ------
        array_like
            affine transformation of x and y

        """
        p = np.array([[self.a, self.b], [self.c, self.d]])
        q = np.array([self.e, self.f])
        xx = np.array([x, y])
        return p.dot(xx)+q

    @staticmethod
    def probability():
        """
        This static method is specific for Barnsley ferns description on how
        to produce a specific pattern. It used a set of probabilities to return
        a pre set AffineTransform object

        Returns
        -------
        Object of type AffineTransform
            A certain affine transform instance
        """
        f1 = AffineTransform(0, 0, 0, 0.16, 0, 0)
        f2 = AffineTransform(0.85, 0.04, -0.04, 0.85, 0, 1.60)
        f3 = AffineTransform(0.20, -0.26, 0.23, 0.22, 0, 1.60)
        f4 = AffineTransform(-0.15, 0.28, 0.26, 0.24, 0, 0.44)
        functions = [f1, f2, f3, f4]
        p1 = 0.01
        p2 = 0.85
        p3 = 0.07
        p4 = 0.07
        p_cumulative = np.array([[0, p1],
                                 [1, p1+p2],
                                 [2, p1+p2+p3],
                                 [3, p1+p2+p3+p4]])
        r = np.random.random()
        for j, p in p_cumulative:
            if r < p:
                return functions[int(j)]

    @classmethod
    def iterate(cls, n):
        """
        This method iterates an x using the AffineTransform objects returned
        from the probability() method to produce a pattern

        Parameters
        ----------
        n : int
            Number of points to produce

        Returns
        -------
        array_like(float, ndim=2, length=n)
            An array of points produced through iteration
        """
        x = np.zeros((n, 2))
        for i in range(n-1):
            mult = AffineTransform.probability()
            x[i+1] = mult(x[i, 0], x[i, 1])
        return x


if __name__ == "__main__":
    xx = AffineTransform.iterate(50000)
    fig = plt.figure(dpi=500)
    ax = plt.subplot(1, 1, 1)
    ax.scatter(*zip(*xx), s=0.1, marker=".", color="red")
    ax.axis("equal")
    plt.savefig("figures/barnsley_fern.png")
    plt.show()

