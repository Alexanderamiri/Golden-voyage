# egen kode
import matplotlib.animation as animation
from ast2000tools.space_mission import SpaceMission
from numpy import pi, cos, sin, sqrt, zeros, size, random, swapaxes, save
import ast2000tools.utils as utils
from ast2000tools.constants import G_sol
import pylab
import concurrent.futures
from matplotlib import rcParams

utils.check_for_newer_version()
rcParams["animation.ffmpeg_path"] = "C:/FFmpeg/bin/ffmpeg.exe"
myseed = 82947
mission = SpaceMission(myseed)
number = 10000000
do = 2 * pi / number
G = 6.67428e-11  # Newton's gravitational constant
AU = 149.6e6 * 1000  # Astronomical unit in metres
timestep = 24 * 3600  # One day in seconds (timestep for the simulation)


class Planet(object):
    """Class to hold information about a planet

    Parameters
    ----------
    n : int
        planet number ie planet order from the star
    mass : float
        mass of planet number n
    starmass : float
        mass of the star the planet orbits
    size : float
        size of the planet
    px, py  : array_like
        array holding the position of the planet
    angles : float
        angle of the planet relativ to the star to a set zero line
    distances: float
        distance of the planet to the star
    esc : float
        eccentricity of the initial orbit
    a : float
        initial semi major axis
    vx, vy : array_like
        arrays holding the velocity of the planet

    """

    def __init__(self, num=0):
        self.n = num
        self.mass = mission.system.masses[self.n]
        self.starmass = mission.system.star_mass
        self.size = None
        self.px = mission.system.initial_positions[0][self.n]
        self.py = mission.system.initial_positions[1][self.n]
        self.angles = mission.system.initial_orbital_angles[self.n]
        self.distances = sqrt(
            mission.system.initial_positions[0][self.n] ** 2
            + mission.system.initial_positions[1][self.n] ** 2
        )
        self.esc = mission.system.eccentricities[self.n]
        self.a = mission.system.semi_major_axes[self.n]
        self.vx = mission.system.initial_velocities[0][self.n]
        self.vy = mission.system.initial_velocities[1][self.n]

    def update_position(self):
        """Analytical position updater

        Returns
        -------
        None
        """
        aa = self.angles
        distance = self.a * (1 - self.esc ** 2) / (1 + self.esc * cos(aa + do))
        self.px = distance * cos(self.angles)
        self.py = distance * sin(self.angles)
        self.distances = distance
        self.angles += do

    def numerical(self):
        """Numerical position of the planet

        Returns
        -------
        None
        """
        steps = number
        time = (
            sqrt(
                mission.system.semi_major_axes[0] ** 3
                / (mission.system.star_mass)
            )
            * 20
        )
        stepsize = time / steps
        self.numposx = zeros(steps)
        self.numposy = zeros(steps)
        self.numposx[0] = self.px
        self.numposy[0] = self.py
        for k in range(steps - 1):
            self.distances = sqrt(self.numposx[k] ** 2 + self.numposy[k] ** 2)

            ax = (
                -G_sol
                * self.starmass
                * self.numposx[k]
                / (self.distances ** 3)
            )
            ay = (
                -G_sol
                * self.starmass
                * self.numposy[k]
                / (self.distances ** 3)
            )

            vx2 = self.vx + ax * stepsize / 2
            vy2 = self.vy + ay * stepsize / 2

            self.numposx[k + 1] = self.numposx[k] + vx2 * stepsize
            self.numposy[k + 1] = self.numposy[k] + vy2 * stepsize

            self.vx = vx2 + ax * stepsize / 2
            self.vy = vy2 + ay * stepsize / 2


def animate(i, bodies, lines):
    """Animation function for orbital animation. Single step

    i : int
        number og planets
    bodies : class
        class of a planet
    lines : array_like
        Animation steps
    Returns
    -------
    array_like
        animation step
    """
    for body in bodies:
        body.update_position()
    for i in range(len(bodies)):
        lines[i].set_data(bodies[i].px, bodies[i].py)
    return lines


def orbits():
    """Calculates the orbits of all the planets

    Returns
    -------
    None
    """
    distances = zeros((8, number))
    angles = zeros((8, number))
    angles[:, 0] = mission.system.initial_orbital_angles
    distances[:, 0] = sqrt(
        mission.system.initial_positions[0] ** 2
        + mission.system.initial_positions[1] ** 2
    )
    for i in range(number):
        for j in range(1):
            esc = mission.system.eccentricities[j]
            a = mission.system.semi_major_axes[j]
            distances[j, i] = (
                a * (1 - esc ** 2) / (1 + esc * cos(angles[j][i - 1] + do))
            )
            angles[j, i] = angles[j][i - 1] + do
    x = distances * cos(angles)
    y = distances * sin(angles)
    for i in range(1):
        pylab.plot(x[i], y[i])


def calculateorbit(thingy):
    """Calculates a single planets numerical orbits

    Parameters
    ----------
    thingy : class
        planet class
    Returns
    -------
        numerical position of input planet
    """
    thingy.numerical()
    return thingy.numposx, thingy.numposy


def planetrbits():
    """Function for animation

    Returns
    -------
    func_class
    """
    for i in range(1):
        (lines[i],) = ax.plot(
            planets[i].px / AU,
            planets[i].py / AU,
            "o-",
            color=planets[i].color,
            ms=planets[i].size,
            label=planets[i].name,
            lw=2,
        )

    return animation.FuncAnimation(
        fig,
        animate,
        frames=2000,
        fargs=[planets, lines],
        interval=16,
        save_count=2000,
    )


if __name__ == "__main__":

    planets = []
    for i in range(1):
        planets.append(Planet(num=i))
    for i in range(1):
        planets[i].size = 10
    lines = [None] * len(planets)

    fig = pylab.figure(figsize=(8, 8))
    ax = pylab.subplot(111)

    orbits()
    # ani = planetorbits()

    ax.set_xlabel("x [AU]")
    ax.set_ylabel("y [AU]")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.plot(0, 0, "o", ms=15, color="r")
    ffwrier = animation.FFMpegWriter(fps=50)
    pylab.title(label="Home Planet Orbit")
    # ani.save('Orbitswithplanets.mp4', writer=ffwrier)
    n = 100000
    nt = 1000
    pos = random.uniform(0, 0.5, [n, 3, nt])
    pylab.show()
