import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as scp


def solutions(sigma):
    """Function to integrate and solve boltzmann equation given sigma

    Parameters
    ----------
    sigma : float
        thermally averaged cross section

    Returns
    -------
    tuple
        x values along with the solved y values for the boltzmann equation
    """
    mx = 1000e9
    sigma_v = sigma
    g = 2
    g_star = 106.75
    yeq0 = (
        9.35e9
        * g
        / 2
        * np.sqrt(100 / g_star)
        * (mx / 1000e9)
        * (sigma_v / 1e-10 * 1e9)
        * 1 ** (3 / 2)
        * np.exp(-1)
    )

    w0 = np.log(yeq0)

    def dw_dx(x, u):
        mx = 1000e9
        g = 2
        g_star = 106.75
        y_eq = (
            9.35e9
            * g
            / 2
            * np.sqrt(100 / g_star)
            * (mx / 1000e9)
            * (sigma_v / 1e-10 * 1e9)
            * x ** (3 / 2)
            * np.exp(-x)
        )
        return (np.exp(2 * np.log(y_eq) - u) - np.exp(u)) * 1 / (x ** 2)

    sol = scp.solve_ivp(dw_dx, [1, 1e3], [w0], method="Radau")
    return sol.t, sol.y


def yy_eq(x, sigma_v):
    mx = 1000e9
    g = 2
    g_star = 106.75
    return (
        9.35e9
        * g
        / 2
        * np.sqrt(100 / g_star)
        * (mx / 1000e9)
        * (sigma_v / 1e-10 * 1e9)
        * x ** (3 / 2)
        * np.exp(-x)
    )


def omega_dm(xf, sigma):
    return 1.69 * np.sqrt(100 / 106.75) * (1e-10 * 1e9 / sigma) * xf / 20


def sampling_routine(range):
    """Find the range where cross sections agree with data plus minus 0.05

    Parameters
    ----------
    range : np.array
        a list of cross section values to examine

    Returns
    -------
    tuple
        upper limit, lower limit on the range of cross section values
    """
    sample_min_sigma = 0
    sample_max_sigma = 0
    for i in range:
        t, y = solutions(i)
        value = y[0][0] * 0.9
        bestval = (np.abs(y1[0] - value)).argmin()
        x_f = t1[bestval]
        omegadm_value = omega_dm(x_f, sigma[0])
        if 0.12 < omegadm_value < 0.17:
            sample_max_sigma = i
        elif 0.07 < omegadm_value < 0.12:
            sample_min_sigma = i
    return sample_max_sigma, sample_min_sigma


sigma = np.array([1e-9, 1e-10, 1e-11]) * 1e9


plt.figure(dpi=400)
t1, y1 = solutions(sigma[0])
value = y1[0][0] * 0.9
bestval = (np.abs(y1[0] - value)).argmin()
x_f = t1[bestval]
print("x_f value {}".format(x_f))
print("difference with observation", np.abs(omega_dm(x_f, sigma[0]) - 0.12))
plt.yscale("log")
plt.xscale("log")
plt.ylim(0.000001)
plt.plot(t1, np.exp(y1[0]))
plt.plot(t1, yy_eq(t1, sigma[0]))
plt.xlabel("x")
plt.ylabel("W")
plt.title("$<\sigma v> = 10^{-9}GeV^{-2}$")
plt.legend(["$y$", "$y_{eq}$"])
plt.show()

plt.figure(dpi=400)
t2, y2 = solutions(sigma[1])
value = y2[0][0] * 0.9
bestval = (np.abs(y2[0] - value)).argmin()
x_f = t1[bestval]
print("x_f value {}".format(x_f))
print("difference with observation", np.abs(omega_dm(x_f, sigma[1]) - 0.12))
plt.yscale("log")
plt.xscale("log")
plt.ylim(0.000001)
plt.plot(t2, np.exp(y2[0]))
plt.plot(t2, yy_eq(t2, sigma[1]))
plt.xlabel("x")
plt.ylabel("W")
plt.title("$<\sigma v> = 10^{-10}GeV^{-2}$")
plt.legend(["$y$", "$y_{eq}$"])
plt.show()

plt.figure(dpi=400)
t3, y3 = solutions(sigma[2])
value = y3[0][0] * 0.9
bestval = (np.abs(y3[0] - value)).argmin()
x_f = t3[bestval]
print("x_f value {}".format(x_f))
print("difference with observation", np.abs(omega_dm(x_f, sigma[2]) - 0.12))
plt.yscale("log")
plt.xscale("log")
plt.ylim(0.000001)
plt.plot(t3, np.exp(y3[0]))
plt.plot(t3, yy_eq(t3, sigma[2]))
plt.xlabel("x")
plt.ylabel("W")
plt.title("$<\sigma v> = 10^{-11}GeV^{-2}$")
plt.legend(["$y$", "$y_{eq}$"])
plt.show()

# Amount of values in cross section range
Steps_in_range = 10000

sigma_range = np.linspace(1e-14, 1e-7, Steps_in_range) * 1e9
s_max, s_min = sampling_routine(sigma_range)
print(
    "range of sigma values,  max {}   min {}".format(s_max / 1e9, s_min / 1e9)
)


""" Run results with current values. Took a good 20 minutes on an i9-9900k CPU

x_f value 11.216236823598155
difference with observation 0.028268195317724315
x_f value 9.678604521936736
difference with observation 0.671563047006415
x_f value 10.493100925308159
difference with observation 8.461764987046601
range of sigma values,  max 0.02001199819981998   min 10.04101309630963


Note that range of sigma values are not in GeV in this output. This was fixed
later on. I recommend turning down
"""
