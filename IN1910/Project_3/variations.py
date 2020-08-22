import numpy as np
import matplotlib.pyplot as plt
from chaos_game import ChaosGame


class Variations:
    """
    A class to produce variations of a figure

    Parameters
    ----------
    x, y, u, v: array_like
        Arrays containing the coordiantes
    colors : String
        String deciding the color of the plot
    plotnumber : int
        a counter for subplots
    """
    def __init__(self, x, y, colors='Black'):
        self.x = x
        self.y = y
        self.colors = colors
        self.plotnumber = 0
        self.u = None
        self.v = None

    def __call__(self, dict):
        """
        Produces a linear combinations of variations with weights

        Parameters
        ----------
        dict :  dictionary
            dictionary where the items is a class object of type Variations
            and the values are weighs

        Returns
        ------
        tuple
            Linear combination of x and y values

        """
        p = 0
        q = 0
        for item, weight in dict.items():
            p += weight*item()[0]
            q += weight*item()[1]
        self.u = p
        self.v = q
        return self.u, self.v

    def linear(self):
        self.u, self.v = self.x, self.y
        return self.u, self.v

    def handkerchief(self):
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        theta = np.arctan2(self.x, self.y)
        self.u, self.v = (r*np.sin(theta+r), r*np.cos(theta-r))
        return self.u, self.v

    def swirl(self):
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        self.u, self.v = x*np.sin(r**2) - y*np.cos(r**2),\
            x*np.cos(r**2) + y*np.sin(r**2)
        return self.u, self.v

    def disc(self):
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        theta = np.arctan2(self.x, self.y)
        self.u, self.v = (np.sin(np.pi*r), np.cos(np.pi*r))*theta/np.pi
        return self.u, self.v

    def diamond(self):
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        theta = np.arctan2(self.x, self.y)
        self.u, self.v = np.sin(theta)*np.cos(r), np.cos(theta)*np.sin(r)
        return self.u, self.v

    def heart(self):
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        theta = np.arctan2(self.x, self.y)
        self.u, self.v = r*(np.sin(theta*r), - np.cos(theta*r))
        return self.u, self.v

    def plot(self, ncol, nrow, cmap='jet'):
        """
        Plots the points stored in u and v and apply a color according to
        colors

        Parameters
        ----------
        cmap : array_like
            colormap to apply
        Returns
        ------
        None
        """
        self.plotnumber += 1
        plt.subplot(nrow, ncol, self.plotnumber)
        plt.scatter(self.u, -self.v, c=self.colors, cmap=cmap, s=0.1)
        plt.axis('equal')
        plt.axis('off')

    @classmethod
    def list_of_variations(cls):
        dict = {'Linear': Variations.linear,
                'Handkercheif': Variations.handkerchief,
                'Swirl': Variations.swirl,
                'Disc': Variations.disc,
                'Diamond': Variations.diamond,
                'Heart': Variations.heart}
        return dict


if __name__ == '__main__':
    a = ChaosGame(4, 1/3)
    a.iterate(10000)
    x = a.x[:, 0]
    y = -a.x[:, 1]
    x /= np.max(np.abs(x), axis=0)
    y /= np.max(np.abs(y), axis=0)
    var = Variations(x, y, a.c)
    weights = np.linspace(0, 1, 4)
    for i in range(len(weights)):
        dic = {var.swirl: weights[i], var.linear: 1-weights[i]}
        var(dic)
        var.plot(2, 2)
        plt.title("linear coef :{:.2} Swirl coef : {:.2}".format(1-weights[i],
                                                           weights[i]))
        print(var.plotnumber)
    plt.show(dpi=500)
