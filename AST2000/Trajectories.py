# egen kode
from ast2000tools.space_mission import SpaceMission
from ast2000tools.constants import G_sol
import numpy as np

G = 6.67428e-11
myseed = 82947
mission = SpaceMission(myseed)


def trajectory(inital_time, inital_pos, inital_vel, T, steps=10000):
    """The trajectory of an object through the system

    Parameters
    -----------
    t : float
        Initial time for the start of the simulation
    x : array_like
        Initial position for the object at the initial time
    v : array_like
        Initial velocity of the object
    T : Float
        Total simulation time
    steps : int
        Total amount of steps in simulation

    Returns
    -------
    array_like
        Final time, final position and final velocity
    """
    planet_positions = np.load("planetpositions.npy", allow_pickle=True)
    planet_masses = mission.system.masses
    planet_radius = mission.system.radii
    starmass = mission.system.star_mass
    t = np.linspace(inital_time, inital_time + T, steps)
    x = np.zeros((steps, 2))
    v = np.zeros((steps, 2))
    x[0] = inital_pos
    v[0] = inital_vel

    print(np.shape(planet_positions))
    for i in range(len(t)):
        dt = t[i + 1] - t[i]
        distances = x[i] - planet_positions[:, :, i]
        acel_planet = (
            -G_sol * planet_masses / (np.linalg.norm(distances, axis=1) ** 3)
        )
        a_list = np.zeros((len(acel_planet), 2))
        a_list[:, 0] = acel_planet
        a_list[:, 1] = acel_planet
        acel_sun = -G_sol * starmass / (np.linalg.norm(x[i]) ** 3)
        v[i + 1] = v[i] + acel_planet * x[i] * dt + acel_sun * x[i] * dt
        x[i + 1] = x[i] + v[i + 1] * dt
    return t[-1], x[-1], v[-1]


def hohmann(r1, m1, r2):
    """Calculate DeltaV required to go from one circular orbit to another

    Parameters
    ----------
    r1 : float
        starting orbit radius
    m1 : float
        mass of primary body
    r2 : float
        Desired orbit radius
    Returns
    float
        The total required DeltaV
    """
    deltav1 = np.sqrt(G * m1 / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)
    deltav2 = np.sqrt(G * m1 / r2) * (1 - np.sqrt(2 * r1 / (r1 + r2)))
    return deltav1 + deltav2


if __name__ == "__main__":
    starmass = mission.system.star_mass * 1.989e30
    d1 = (
        np.sqrt(
            mission.system.initial_positions[0][0] ** 2
            + mission.system.initial_positions[1][0] ** 2
        )
        * 1.496e11
    )
    d1_radius = mission.system.radii[0]
    d1_mass = mission.system.masses[0] * 1.989e30
    d1_esc = np.sqrt(2 * G * d1_mass / (d1_radius * 1e3))
    d2 = (
        np.sqrt(
            mission.system.initial_positions[0][1] ** 2
            + mission.system.initial_positions[1][1] ** 2
        )
        * 1.496e11
    )
    d2_radius = mission.system.radii[1]
    d2_mass = mission.system.masses[1] * 1.989e30
    d2_esc = np.sqrt(2 * G * d2_mass / (d2_radius * 1e3 + 600e3))
    l = (d2) * np.sqrt(d2_mass / (starmass * 10))
    targetorbit = hohmann(d1, starmass, d2)
    targetplanetorbit = hohmann(l / 10, d2_mass, l)
    print("mass of home planet {:.3e}".format(d1_mass))
    print("radius of home planet {:.3e}".format(d1_radius))
    print("mass of target planet {:.3e}".format(d2_mass))
    print("radius of target planet {:.3e}".format(d2_radius))
    print("mass of star {:.3e}".format(starmass))
    print(
        "Distance we need to be within to circularize {:.3f} km".format(
            l / 1e3
        )
    )
    print("home planet distance {:.3e} ".format(d1))
    print("target planet distance {:.3e}".format(d2))
    print("home planet distance {:.3e} ".format(d1 / 1.496e11))
    print("target planet distance {:.3e}".format(d2 / 1.496e11))
    print("DeltaV to escape home planet {:.3f} km/s".format(d1_esc / 1e3))
    print(
        "DeltaV to match target planets orbit {:.3f} km/s".format(
            targetorbit / 1e3
        )
    )
    print(
        "DeltaV to enter circular orbit at target {:.3f} km/s".format(
            targetplanetorbit / 1e3
        )
    )
    print(
        "Total DeltaV required {:.3f} km/s".format(
            (d1_esc + targetorbit + targetplanetorbit) / 1e3
        )
    )
