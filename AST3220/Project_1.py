import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit


def luminosity_distance(z, omega_a0, omega_m0):
    omega_k0 = 1 - omega_m0 - omega_a0
    H_0 = 0.07

    def hubble(t, x):
        return H_0 * np.sqrt(
            (omega_m0 * (1 + t) ** 3 + omega_k0 * (1 + t) ** 2 + omega_a0)
        )

    # Making sure RHS is positive
    fried = omega_m0 * (1 + z) ** 3 + omega_k0 * (1 + z) ** 2 + omega_a0
    if fried.all() > 0:
        steps = 1000
        sol = 0
        dt = z / steps
        for i in range(steps + 1):
            sol += dt * H_0 / (hubble(i * dt, 0))
        # For different curvature parameters
        if omega_k0 > 0:
            dl = (
                (1 + z)
                / (np.sqrt(abs(omega_k0)))
                * np.sin(np.sqrt(abs(omega_k0)) * sol)
            )
            return dl * 300 / 70
        elif omega_k0 < 0:
            dl = (
                (1 + z)
                / (np.sqrt(abs(omega_k0)))
                * np.sinh(np.sqrt(abs(omega_k0)) * sol)
            )
            return dl * 300 / 70
        elif omega_k0 == 0:
            dl = (1 + z) * sol
            return dl * 300 / 70
    else:
        print("rhs of friedman equation was not positive")


def luminosity_dgp(z, omega_rc, omega_m0):
    omega_k0 = (
        1
        - 2 * omega_rc
        - omega_m0
        - 2 * np.sqrt(omega_rc) * np.sqrt(omega_m0 + omega_rc)
    )
    H_0 = 0.07

    def hubble(t, x):
        return H_0 * np.sqrt(
            (np.sqrt(omega_m0 * (1 + z) ** 3 + omega_rc) + np.sqrt(omega_rc))
            ** 2
            + omega_k0 * (1 + z) ** 2
        )

    # Making sure RHS is positive
    fried = (
        np.sqrt(omega_m0 * (1 + z) ** 3 + omega_rc) + np.sqrt(omega_rc)
    ) ** 2 + omega_k0 * (1 + z) ** 2
    if fried.all() > 0:
        steps = 1000
        sol = 0
        dt = z / steps
        for i in range(steps + 1):
            sol += dt * H_0 / (hubble(i * dt, 0))
        # For different curvature parameters
        if omega_k0 > 0:
            dl = (
                (1 + z)
                / (np.sqrt(abs(omega_k0)))
                * np.sin(np.sqrt(abs(omega_k0)) * sol)
            )
            return dl * 300 / 70
        elif omega_k0 < 0:
            dl = (
                (1 + z)
                / (np.sqrt(abs(omega_k0)))
                * np.sinh(np.sqrt(abs(omega_k0)) * sol)
            )
            return dl * 300 / 70
        elif omega_k0 == 0:
            dl = (1 + z) * sol
            return dl * 300 / 70
    else:
        print("rhs of friedman equation was not positive")


def probability(file):
    # Reading data from file
    f = open(file)
    for _ in range(5):
        f.readline()
    z = []
    dl = []
    sig = []
    for line in f:
        z.append(float(line.split()[0]))
        dl.append(float(line.split()[1]))
        sig.append(float(line.split()[2]))
    z = np.array(z)
    dl = np.array(dl)
    sig = np.array(sig)
    # Chi squared optimizing
    omega_m = np.linspace(0, 2, 20)
    omega_a = np.linspace(0, 2, 20)
    chi = []
    val = []
    chi_dgp = []
    for m in omega_m:
        for a in omega_a:
            sigma = 0
            sigma_dgp = 0
            for i in range(len(z)):
                sigma += ((luminosity_distance(z[i], a, m) - dl[i]) ** 2) / (
                    sig[i] ** 2
                )
                sigma_dgp += ((luminosity_dgp(z[i], a, m) - dl[i]) ** 2) / (
                    sig[i] ** 2
                )
            chi.append(sigma)
            chi_dgp.append(sigma_dgp)
            val.append([a, m])
    chi = np.array(chi)
    val = np.array(val)
    chi_dgp = np.array(chi_dgp)
    # Finding Chi_min
    chimin = 10000
    chimin_dgp = 10000
    index = 0
    index_dgp = 0

    for i in range(len(z)):
        if chi[i] < chimin:
            index = i
            chimin = chi[i]
        if chi_dgp[i] < chimin_dgp:
            index_dgp = i
            chimin_dgp = chi_dgp[i]

    k = (chi[:] - chi[index]) < 6.17
    k_dgp = (chi_dgp - chi_dgp[index_dgp]) < 6.17
    print("ACDM chi squared with parameters", chi[index], val[index])
    print(
        "dgp chi_min squared with parameters",
        chi_dgp[index_dgp],
        val[index_dgp],
    )

    # Plot of Chi^2 - chi^2_min < 6.17 for ACDM
    plt.figure(dpi=500)
    for i in range(len(val[k])):
        plt.plot(val[k][i][1], val[k][i][0], "o", color="red")
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.xlabel("$\Omega_{m0}$")
    plt.ylabel("$\Omega_{a0}$")
    plt.title("Parameter optimization ACDM")
    plt.legend(["$\chi^{2}(p)-\chi^{2}_{min} < 6.17)$"])
    plt.show()
    # Plot of Chi^2 - chi^2_min < 6.17 for DGP
    plt.figure(dpi=500)
    for i in range(len(val[k_dgp])):
        plt.plot(val[k_dgp][i][1], val[k_dgp][i][0], "o", color="red")
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.xlabel("$\Omega_{m0}$")
    plt.ylabel("$\Omega_{rc}$")
    plt.title("Parameter optimization DGP")
    plt.legend(["$\chi^{2}(p)-\chi^{2}_{min} < 6.17)$"])
    plt.show()
    # Plot of DGP vs data
    plt.figure(dpi=500)
    plt.plot(z, luminosity_dgp(z, 0, 0.2020202))
    plt.errorbar(z, dl, yerr=sig, fmt=".", capsize=2)
    plt.legend(["DGP $\Omega{m0}= 0.1, \Omega{rc}= 0.2020202$", "Data"])
    plt.title("Luminosity distance DGP")
    plt.xlabel("Redshift z")
    plt.ylabel("Gpc")
    plt.show()
    # Plot of different models vs data
    plt.figure(dpi=500)
    plt.errorbar(z, dl, yerr=sig, fmt=".", capsize=2)
    plt.plot(z, luminosity_distance(z, 0, 1))
    plt.plot(z, luminosity_distance(z, 1, 0))
    plt.plot(z, luminosity_dgp(z, 0, 0.2020202))
    plt.plot(z, luminosity_distance(z, 0.27586207, 1.72413793))
    plt.plot(z, luminosity_distance(z, 0.34482759, 1.93103448))
    plt.legend(
        [
            "EdS",
            "dS",
            "DGP $\Omega{m0}= 0.1, \Omega{rc}= 0.2020202$",
            "ACDM $\Omega{m0}= 1.724, \Omega{a0}= 0.275$",
            "ACDM $\Omega{m0}= 1.931, \Omega{a0}= 0.344$",
            "Data",
        ]
    )
    plt.title("Luminosity distance")
    plt.xlabel("Redshift z")
    plt.ylabel("Gpc")
    plt.show()


probability("sndata.txt")
