from numpy import *
from matplotlib.pyplot import *

R = 8.314
m = [0.028, 0.002, 0.004]
t = array([300, 600, 1000])

V = linspace(0, 2000, 10000)
v_1 = linspace(0, 300, 10000)


def d(v, T):
    """Differentiates velocity over time

    Parameters
    ---------
    v : float, array
        Volume
    T : float, array
        Time
    Returns
    -------
    np.array
    """
    return (
        (m[0] / (2 * pi * R * T)) ** (3 / 2)
        * 4
        * pi
        * v ** 2
        * e ** (-((m[0] * v ** 2) / (2 * R * T)))
    )


def plots():
    """Plots everything"""
    xlabel("v[m/s]")
    ylabel("Probability")
    legend(["300K", "600K"])
    title("Maxwell-Boltzmann distribution")
    plot(V, d(V, t[0]))
    plot(V, d(V, t[1]))
    show()


def probability300():
    """Probability that the velocity is over 300"""
    return trapz(v_1, d(v_1, t[0]))


def probability11000(vmin, M, t, eps=1e-5, i=1e3):
    """Probability that the velocity is over 11000

    Parameters
    ----------
    vmin : float
        Minimum velocity
    M : float, array
        Mass
    t : float, array
        Time
    eps : float
        Condition minimum value
    i : int
        Number of steps

    Returns
    -------
    float
    """
    tot = 0
    dx = 1e-16
    vrms = sqrt(3 * R * t / M)
    x = vmin / sqrt(2 * R * t / M)
    n = 0
    m = 0
    while n < i:
        x += dx
        x2 = x ** 2
        term = x2 * exp(-x2)
        if term < eps:
            m += 1
            if m > 1e2:
                break
        else:
            m = 0
        tot += term
        n += 1
    return tot


plots()
print(
    "Probability of less than 300 m/s for n2 is {:.5f} %".format(
        probability300() * 100
    )
)
print(
    "Probability of more than 11000 m/s for n2 is {:.3e} %".format(
        probability11000(11e3, m[0], t[2]) * 100
    )
)
print(
    "Probability of more than 11000 m/s for h2 is {:.3e} %".format(
        probability11000(11e3, m[1], t[2]) * 100
    )
)
print(
    "Probability of more than 11000 m/s for he2 is {:.3e} %".format(
        probability11000(11e3, m[2], t[2]) * 100
    )
)
print(
    "Probability of more than 2400 m/s for n2 is {:.3f} %".format(
        probability11000(2.4e3, m[0], t[2]) * 100
    )
)
