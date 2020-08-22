from PIL import Image
import numpy as np
from ast2000tools.space_mission import SpaceMission
from sympy import geometry

myseed = 82947
mission = SpaceMission(myseed)
img = Image.open("sample0000.png")
pixels = np.array(img)
sky = np.load("himmelkule.npy")
fov = [70, 70]
xmm = [
    -2 * np.sin(fov[1] / 2) / (1 + np.cos(fov[1] / 2)),
    2 * np.sin(fov[1] / 2) / (1 + np.cos(fov[1] / 2)),
]
ymm = [
    -2 * np.sin(fov[1] / 2) / (1 + np.cos(fov[0] / 2)),
    2 * np.sin(fov[1] / 2) / (1 + np.cos(fov[0] / 2)),
]
x = np.linspace(xmm[0], xmm[1], len(pixels[0, :]))
y = np.linspace(xmm[0], xmm[1], len(pixels[:, 0]))
X, Y = np.meshgrid(x, y)
XY = np.zeros((480, 640, 2))
XY[:, :, 0] = X
XY[:, :, 1] = Y
proj = np.zeros((360, 480, 640, 3), dtype=np.uint8)
for j in range(359):
    phi0 = j * np.pi / 180
    rho = np.sqrt(X ** 2 + Y ** 2)
    c = 2 * np.arctan(rho / 2)
    theta = np.pi / 2 - np.arcsin(
        np.cos(c) * np.cos(np.pi / 2) + Y * np.sin(c) * np.sin(np.pi / 2) / rho
    )
    phi = phi0 + np.arctan(
        X
        * np.sin(c)
        / (
            rho * np.sin(np.pi / 2) * np.cos(c)
            - Y * np.cos(np.pi / 2) * np.sin(c)
        )
    )
    for n, (i, v) in enumerate(zip(theta, phi)):
        for m, (k, w) in enumerate(zip(i, v)):
            pixminimum = SpaceMission.get_sky_image_pixel(k, w)
            temp = sky[pixminimum]
            proj[j][n][m] = (temp[2], temp[3], temp[4])
np.save("Skyprojections.npy", proj)
img.show()


def findphi(picture):
    """Takes a single image and find its the angle in an reference map

    Parameters
    ----------
    picture : str
        Image file name to look for

    Returns
    -------
    float
        Angle phi of where the picture is on the skymap
    """
    im = Image.open(picture)
    pixels = np.array(im)
    proj = np.load("Skyprojections.npy")
    diff = np.zeros(360)
    for i in range(359):
        diff[i] = np.sum((proj[i] - pixels) ** 2)
    phi = diff.argmin()
    return phi


def velocity_refstars(vref1, vref2):
    """

    Parameters
    ----------
    vref1 : velocity of first reference star
    vref2 : velocity of second reference star

    Returns
    -------
    float
        The speed in reference to the reference stars
    """
    wavelength = 656.3
    phi_1, phi_2 = mission.star_direction_angles()
    lambd1, lambd2 = mission.star_doppler_shifts_at_sun
    vrefstar1 = lambd1 * 1e8 / wavelength
    vrefstar2 = lambd2 * 1e8 / wavelength
    vel1 = vref1 * 1e8 / wavelength
    vel2 = vref2 * 1e8 / wavelength
    relvelocity1 = vrefstar1 - vel1
    relvelocity2 = vrefstar2 - vel2
    rm = np.array(
        [[np.sin(phi_2), -np.sin(phi_1)], [-np.cos(phi_2), np.cos(phi_1)]]
    )
    vm = np.array([[relvelocity1], [relvelocity2]])
    vxy = (1 / np.sin(phi_2 - phi_1) * rm * vm) * 0.000210945021
    return vxy


def position(distances, coordinates):
    """Finds position in solar system in reference to the planets in the system

    Parameters
    ----------
    distances : array_like()
        Distances to each planet in the system
    coordinates : array_like()
         coordinates of the planets in the system
    Returns
    -------
    array_like
        position relative to the input planets
    """
    circles = []
    for i in distances:
        circles.append((geometry.Circle(coordinates[i], distances[i])))
    intersect = np.zeros((len(circles), 2))
    for i in range(0, len(circles) - 3, 2):
        inter = np.array(geometry.intersection(circles[i], circles[i + 1]))
        for k in range(2):
            intersect[i + k] = inter[k]
    pt1 = 0
    pt2 = 0
    for i in range(2, len(intersect)):
        pt1 += np.sum((intersect[0] - intersect[i]) ** 2)
        pt2 += np.sum((intersect[1] - intersect[i]) ** 2)
    if pt1 < pt2:
        return intersect[0, 0], intersect[0, 1]
    else:
        return intersect[1, 0], intersect[1, 1]
