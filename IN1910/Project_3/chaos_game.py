import numpy as np
import matplotlib.pyplot as plt


class ChaosGame:
    """
    A class to make n dimensional polygon and generate a pattern of points
    within the polygon

    Parameters
    ----------
    n: int
        Number of vertices in the polygon
    r : float
        The constant used in making the pattens
    Attributes
    ----------
    n, r : see parameters

    vertices : array_like(float, ndim=2, length=n)
        This is an array containing each of the corners in the polygon

    x : array_like(float, ndim=2)
        This array contains random points generated through an algorithm using
        the parameter r and the vertices stored in the array vertices

    indices : array_like(float, ndim=1)
        This is an array with the indices of which corner was used to generate
        a given point in x

    Raises
    ------
    ValueError
        You've entered invalid values, n >= 3, 0 < r < 1
        The variable color must be boolean

    TypeError
        Either n is not an integer or r is not float
    """
    def __init__(self, n=3, r=0.5):
        if isinstance(n, int) and isinstance(r, float):
            if n >= 3 and (0 < r < 1):
                self.n = n
                self.r = r
                self._generate_ngon()
                self._starting_point()
            else:
                raise ValueError(
                    "You've entered invalid values, n >= 3, 0 < r < 1")
        else:
            raise TypeError(
                "Either n is not an integer or r is not float")

    def _generate_ngon(self):
        theta = np.linspace(0, 2*np.pi, self.n+1)
        self.vertices = np.array([[np.sin(i), np.cos(i)] for i in theta[:-1]])

    def _starting_point(self):
        r = [np.random.random() for _ in range(self.n)]
        weights = [i/sum(r) for i in r]
        self._starting_point = sum([weights[i]*self.vertices[i]
                                    for i in range(self.n)])

    def iterate(self, steps, discard=5):
        """A method to generate random points within the ngon

        Parameters
        ----------
        steps : int
            Amount of steps/points to generate
        discard : int
            Amount of points to discard for the initial array

        Returns
        -------
        None
        """
        starts = np.zeros((discard, 2))
        self.x = np.zeros((steps, 2))
        self.indices = np.zeros(steps)
        starts[0] = self._starting_point
        for i in range(discard-1):
            starts[i+1] = self.r*starts[i]+(1-self.r)*self.vertices[
                np.random.randint(self.n)]
        self.x[0] = starts[-1]
        for i in range(steps-1):
            self.indices[i] = np.random.randint(self.n)
            self.x[i+1] = self.r*self.x[i]+(1-self.r)*self.vertices[
                int(self.indices[i])]
        self._compute_color()

    def _compute_color(self):
        length = len(self.indices)
        self.c = np.zeros(length)
        self.c[0] = self.indices[0]
        for i in range(length-1):
            self.c[i+1] = (self.c[i]+self.indices[i+1])*0.5
        return self.c

    def plot_ngon(self):
        """
        Plots and calls show() for the ngon's vertices
        """
        fig = plt.figure(dpi=500)
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(*zip(*self.vertices))
        ax.axis('equal')
        plt.show()

    def plot(self, color=False, cmap='jet'):
        """
        Plots the points stored in x and apply a color according the the boolean
        color
        Parameters
        ----------
        color : boolean
            If set to true it will assign a gradient using cmap to the points,
            if set to false(default) it will plot them with the color black

        cmap : array_like
            colormap to apply
        Returns
        ------
        None
        """
        if color:
            colors = self._compute_color()
        elif not color:
            colors = 'black'
        try:
            fig = plt.figure(dpi=500)
            ax = fig.add_subplot(1, 1, 1)
            ax.scatter(*zip(*self.x), c=colors, cmap=cmap, s=0.1, marker='.')
            ax.axis('equal')
        except ValueError:
            print("The variable color must be boolean")

    def show(self, color=False, cmap='jet'):
        """
        Call ChaosGame.plot() and show() to show the plotted points

        Parameters
        ----------
        color, cmap : see ChaosGame.plot() for documentation

        Returns
        ------
        None
        """
        self.plot(color, cmap)
        plt.show()

    def savepng(self, outfile, color=False, cmap='jet'):
        """
        Call ChaosGame.plot() and savefig() to save the plotted points

        Parameters
        ----------
        outfile : String
            String containing the outputfile name

        color, cmap : see ChaosGame.plot() for documentation

        Returns
        ------
        None
        """
        self.plot(color, cmap)
        plt.savefig(outfile)


if __name__ == "__main__":
    a = ChaosGame(3, 2/3)
    a.iterate(10000)
    a.show(color=True)
    #a.savepng("figures/chaos5.png", color=True)
