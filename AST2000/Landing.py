from ast2000tools.space_mission import SpaceMission
import numpy as np

G = 6.67428e-11
myseed = 82947
mission = SpaceMission(myseed)


def landing(x, v, radius, M, m, cd, rho, area, w, dt):
    """Calculates a descent through an atmosphere

    Parameters
    ----------
    x : array_like
        Initial position of the spacecraft
    v : array_like
        Initial velocity of the spacecraft
    radius : float
        Radius of the planet
    M : float
        Mass of the planet
    m : float
        Mass of the spacecraft
    cd : float
        Drag coefficient
    rho : float
        Density of air
    area : float
        Cross section of the spacecraft moving through the atmosphere
    w : float
        Wind speed
    dt : float
        time step
    Returns
    -------
    tuple
        Returns (position, velocity, time)
        The calculated velocity at impact and the position as well as how long it took
    """
    t = 0
    r = np.linalg.norm(x)
    v_w = v + w
    while x > radius:
        if r <= 5000:
            area += 50
            fgx = -G * M * m * x / (r ** 3)
            fd = 0.5 * cd * rho * area * (v_w ** 2)
            acel = (fgx - fd) / m
            v -= acel * dt
            x -= v * dt
        elif r > 5000:
            t += dt
            fgx = -G * M * m * x / (r ** 3)
            fd = 0.5 * cd * rho * area * (v_w ** 2)
            acel = (fgx - fd) / m
            v -= acel * dt
            x -= v * dt
    return x, v, t
