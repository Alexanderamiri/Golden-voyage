import numpy as np
import matplotlib.pyplot as plt
from numba import jit


@jit(nopython=True)
def solver(
    initial_Y,
    t0,
    T,
    stepsize,
    rho,
    n_mass_rate,
    n_droplet,
    spring_constant_k,
    friction,
    mass_Rate,
    g,
    threshold,
    alpha,
):
    """Function to produce droplet periods of water drops.

    Parameters
    ----------
    initial_Y : ndarray
        Initial values for [position, velocity, mass]
    t0 : float
        Start time
    T : float
        End time
    stepsize : float
    rho : float
        Density of water
    n_mass_rate : float
        Number of mass flow rates
    n_droplet : float
        Number of water droplets
    spring_constant_k : float
        Stiffness of a spring, in this case the effect of surface tension
    friction : float
        frictional coefficient
    mass_Rate : float
        Rate of Flow starting point
    g : float
        Gravitational acceleration
    threshold : float
        The threshold
    alpha : float
        The flow rate coefficient

    Returns
    -------
    ndarray
        Array of drop periods
    """
    y0 = initial_Y
    t0 = t0
    T = T
    dt = stepsize
    rho = rho
    nR = n_mass_rate
    nD = n_droplet
    k = spring_constant_k
    b = friction
    rr = mass_Rate
    g = g
    x_t = threshold
    alpha = alpha

    def f(u, r):
        """Differential equations

        Parameters
        ----------
        u : ndarray
            Function values
        r : float
            Rate of flow

        Returns
        -------
        ndarray
            Derivatives
        """
        y = np.zeros(u.size)
        y[0] = u[1]
        y[1] = -k / u[2] * u[0] - (b + r) / u[2] * u[1] + g
        y[2] = r
        return y

    def rungekutta_4(y, r):
        """Function to a step using rungekutta4

        Parameters
        ----------
        y : ndarray
            Function values
        r : float
            Rate of flow

        Returns
        -------
        ndarray
            Next step
        """
        x1 = f(y, r)
        h_1 = y + x1 * dt / 2
        x2 = f(h_1, r)
        h_2 = y + x2 * dt / 2
        x3 = f(h_2, r)
        h_3 = y + x3 * dt
        x4 = f(h_3, r)
        tm = (x1 + 2 * x2 + 2 * x3 + x4) / 6
        return y + tm * dt

    def integrate(r):
        """Function to integrate the differential equations and form droplets

        Parameters
        ----------
        r : float
            Rate of flow

        Returns
        -------
        ndarray
            time, solution to equations, drop times, drop rates
        """
        N = np.int((T - t0) / dt)
        t = np.zeros(N)
        t[0] = t0
        sol = np.zeros((N, y0.size))
        sol[0] = y0
        td = np.zeros(N)
        dtd = np.zeros(N)
        dcnt = 0
        for i in range(1, N):
            t[i] = t[i - 1] + dt
            sol[i] = rungekutta_4(sol[i - 1], r)
            if sol[i, 0] > x_t:
                _dx = x_t - sol[i - 1, 0]
                _dt = _dx / sol[i - 1, 1]
                t[i] = t[i - 1] + _dt
                sol[i] = rungekutta_4(sol[i - 1], r)
                dm = alpha * sol[i, 1] * sol[i, 2]
                if dm >= sol[i, 2]:
                    dm = sol[i, 2] - 1e-5
                dx = (3 * dm ** 4 / (4 * np.pi * rho * sol[i, 2] ** 3)) ** (
                    1 / 3
                )
                sol[i, 0] -= dx
                sol[i, 2] -= dm
                td[dcnt] = t[i]
                if dcnt > 0:
                    dtd[dcnt] = td[dcnt] - td[dcnt - 1]
                dcnt += 1
        td = td[0:dcnt]
        dtd = dtd[0:dcnt]
        return t, sol, td, dtd

    def drops():
        """Function to find drop periods

        Returns
        -------
        ndarray
            Water drop periods
        """
        dtds = np.zeros((nR, nD))
        for i in range(nR):
            print(rr[i])
            ts, sol, td, dtd = integrate(rr[i])
            dtds[i, :] = dtd[-nD - 1 : -1]
        return dtds

    return drops()


dt = 1e-4
y00 = np.array([0, 0.001, 0.00001])
kk = 0.475
bb = 0.001
g = 9.81
xc = 0.0025
alpha = 50
rhoo = 1000
nR = 1001
nD = 60
Rs = 0.00055 + np.arange(nR) / (nR - 1) * 0.0002

droplet = solver(
    initial_Y=y00,
    t0=0,
    T=20,
    stepsize=dt,
    rho=rhoo,
    n_mass_rate=nR,
    n_droplet=nD,
    spring_constant_k=kk,
    friction=bb,
    mass_Rate=Rs,
    g=g,
    threshold=xc,
    alpha=alpha,
)


plt.figure(figsize=[12, 6], dpi=500)
for i in range(nD):
    plt.scatter(Rs * 1e3, droplet[:, i], s=1, alpha=0.4, c="black")
plt.xlim((0.550, 0.750))
plt.ylim((0.09, 0.16))
plt.xlabel("R [g/s]")
plt.ylabel("period [s]")
plt.show()


plt.figure(figsize=[6, 6], dpi=500)
for i in range(nD):
    fft = np.fft.rfft(droplet[:, i]) / nR  # Amplitude
    frek = np.fft.rfftfreq(len(Rs), Rs[1] - Rs[0])  # Frequency
    plt.plot(frek, np.abs(fft))
plt.xlim((0, 100))
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.show()

plt.figure(figsize=[6, 6], dpi=500)
FS = np.fft.fftn(droplet)
plt.pcolormesh(np.log(np.abs(np.fft.fftshift(FS)) ** 2))
plt.colorbar()
plt.show()
