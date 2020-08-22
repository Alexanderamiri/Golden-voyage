import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from Project1 import StellarCore


class Star(StellarCore):
    def __init__(self, T, rho, r, l, m, sanity=False):
        """This class will simulate energy transport through a star

        Parameters
        ----------
        self.T : float
            Temperature of the core
        self.rho : float
            Density of the core
        self.X : float
            Mass fraction of hydrogen
        self.Y_He3: float
            Mass fraction of Helium3
        self.Y : float
            Mass fraction of helium
        self.Z_Li7 : float
            Mass fraction of Li7
        self.Z_Be7 : float
            Mass fraction of Be7
        self.Z_N14: float
            Mass fraction of N14
        self.avgmass : float
            Average mass of particles present in the star
        """
        self.T_0 = T
        self.rho_0 = rho
        self.r_0 = r
        self.l_0 = l
        self.m_0 = m
        self.X = 0.7
        self.Y_He3 = 1e-10
        self.Y = 0.29
        self.Z_Li7 = 1e-7
        self.Z_Be7 = 1e-7
        self.Z_N14 = 1e-11
        self.avgmass = 1 / (
            2 * self.X
            + 3 / 4 * self.Y
            + 6 / 7 * self.Z_Be7
            + 4 / 7 * self.Z_Li7
            + 9 / 14 * self.Z_N14
        )
        self.c = 3e8
        self.m_u = 1.6605e-27
        self.N_a = 6.0221e23
        self.mev_to_j = 1.6022e-13
        self.kb = 1.38064852e-23
        self.skb = 5.67e-8
        self.G = 6.67408e-11
        self.a = 4 * self.skb / self.c
        self.N = 1 / (self.avgmass * self.m_u)
        self.cp = 5 / 2 * self.N * self.kb
        self.alpha = 1
        self.delta = 1
        self.nabla_ad = 2 / 5
        if sanity:
            print("Checking for sanity")
            self.Sanity_check()

    def kappa_finder(self, t, rho, file):
        """Calculates opacity given temperature and density.

        Interpolates if the values given does not match the input file's 
        range of values for log_!0(T) and log_10( rho*1e-3 / ( (t*1e-6)**3 )

        Parameters
        ----------
        t : float
            Temperature in Kelvin
        rho : float
            Density in kg/m3
        file : string
            Text file to read for opacity values

        Returns
        -------
        float
            Opacity value in m2/kg
        """
        r_val = np.log10((rho * 1e-3) / ((t * 1e-6) ** 3))
        t_val = np.log10(t)
        data = np.genfromtxt(file)
        log_T = data[1:, 0]
        log_R = data[0, 1:]
        log_k = data[1:, 1:]

        interpoll = interpolate.interp2d(log_R, log_T, log_k)
        k_val = 10 ** interpoll(r_val, t_val) * 0.1
        # if not (log_T[0] <= t_val <= log_T[-1]):
        #     print('T values out of bounds')
        # elif not (log_R[0] <= r_val <= log_R[-1]):
        #     print('R values out of bounds',r_val)
        return k_val

    def _rho(self, P, T):
        """Calculates the density given the pressure and temperature.
        
        Parameters
        ----------
        P : float
            Pressure in pascal
        T : float
            Temperature in kelvin
        Returns
        -------
        float
            Density
        """
        return (
            self.avgmass * self.m_u * (P - T ** 4 * self.a / 3) / (self.kb * T)
        )

    def _pressure(self, rho, T):
        """Calculates the pressure given the density and temperature.


        Parameters
        ----------
        rho : float
            Density in kg/m3
        T : float
            Temperature in kelvin
        """
        P_G = rho * self.kb * T / (self.m_u * self.avgmass)
        P_rad = T ** 4 * self.a / 3
        P = P_G + P_rad
        return P

    def u(self, t, rho, k, g, H_p):
        uu = (
            (64 * self.skb * t ** 3)
            / (3 * k * (rho ** 2) * self.cp)
            * np.sqrt(H_p / (g * self.delta))
        )
        return uu

    def f_radius(self, r, rho):
        return 1 / (4 * np.pi * r ** 2 * rho)

    def f_pressure(self, r, m):
        return (self.G * m) / (4 * np.pi * r ** 4)

    def f_t(self, k, L, r, T):
        return (3 * k * L) / (256 * np.pi ** 2 * self.skb * r ** 4 * T ** 3)

    def convection(self, t, rho, g, hp, xi):
        return (
            rho
            * self.cp
            * t
            * np.sqrt(g * self.delta)
            * hp ** (-3 / 2)
            * (hp / 2) ** 2
            * xi ** 3
        )

    def radiation(self, t, rho, k, hp, nabla_stable, fc):
        return 16 * self.skb * t ** 4 * nabla_stable / (3 * k * rho * hp) - fc

    def nabla_stable(self, t, rho, r, l, k, h_p):
        nn = (
            3
            * k
            * l
            * rho
            * h_p
            / (64 * np.pi * self.skb * (t ** 4) * (r ** 2))
        )
        return nn

    def flux(self, l, r):
        return l / (4 * np.pi * r ** 2)

    def x_i(self, hp, u, nabla_ad, nabla_stable):
        w = u / (hp ** 2)
        x = np.roots([1 / w, 1, 2 * w, (nabla_ad - nabla_stable)])
        for i in range(len(x)):
            if np.isreal(x[i]):
                return np.real(x[i])

    def gravity(self, m, r):
        return self.G * m / (r ** 2)

    def h_p(self, t, g):
        return self.N * self.kb * t / g

    def nabla_star(self, hp, xii, u):
        return xii ** 2 + 2 * u / (hp ** 2) * xii + self.nabla_ad

    def intergrate(self, max_step_size):
        """Integrates the four differential equations that govern the star"""

        t = [self.T_0]
        r = [self.r_0]
        l = [self.l_0]
        m = [self.m_0]
        rho = [self.rho_0]

        p = [self._pressure(rho[-1], t[-1])]
        # self.P_0 = p
        kappa = self.kappa_finder(t[-1], rho[-1], "opacity.txt")
        g = self.gravity(m[-1], r[-1])
        H_p = self.h_p(t[-1], g)

        nabla_stable = [
            self.nabla_stable(t[-1], rho[-1], r[-1], l[-1], kappa, H_p)
        ]
        u = self.u(t[-1], rho[-1], kappa, g, H_p)
        xii = self.x_i(H_p, u, self.nabla_ad, nabla_stable[-1])
        nabla_s = [self.nabla_star(H_p, xii, u)]
        fc = [self.convection(t[-1], rho[-1], g, H_p, xii)]
        fr = [
            self.radiation(
                t[-1], rho[-1], kappa, H_p, nabla_stable[-1], fc[-1]
            )
        ]

        star = StellarCore(t[-1], rho[-1])
        star.rates()
        pp1 = [star.PPI()]
        pp2 = [star.PPII()]
        pp3 = [star.PPIII()]
        cno = [star.CNO()]
        epsilon = [star.epsilon()]

        non_zero = True
        i = 0
        while non_zero:
            _ = StellarCore(t[-1], rho[-1])
            _.rates()
            pp1.append(_.PPI())
            pp2.append(_.PPII())
            pp3.append(_.PPIII())
            cno.append(_.CNO())
            epsilon.append(_.epsilon())

            g = self.gravity(m[-1], r[-1])
            kappa = self.kappa_finder(t[-1], rho[-1], "opacity.txt")

            H_p = self.h_p(t[-1], g)
            u = self.u(t[-1], rho[-1], kappa, g, H_p)
            xii = self.x_i(H_p, u, self.nabla_ad, nabla_stable[-1])

            nabla_stable.append(
                self.nabla_stable(t[-1], rho[-1], r[-1], l[-1], kappa, H_p)
            )
            nabla_s.append(self.nabla_star(H_p, xii, u))

            dp = -self.f_pressure(r[-1], m[-1])
            dr = self.f_radius(r[-1], rho[-1])
            dl = epsilon[-1]

            if nabla_stable[-1] > self.nabla_ad:
                fc.append(self.convection(t[-1], rho[-1], g, H_p, xii))
                fr.append(
                    self.radiation(
                        t[-1], rho[-1], kappa, H_p, nabla_stable[-1], fc[-1]
                    )
                )
                dt = -nabla_s[-1] / (4 * np.pi * rho[-1] * (r[-1] ** 2))

            else:
                fc.append(0)
                fr.append(
                    self.radiation(
                        t[-1], rho[-1], kappa, H_p, nabla_stable[-1], fc[-1]
                    )
                )
                dt = -self.f_t(kappa, l[-1], r[-1], t[-1])

            dr_min = max_step_size * r[-1] / dr
            dp_min = max_step_size * p[-1] / dp
            dl_min = max_step_size * l[-1] / dl
            dt_min = max_step_size * t[-1] / dt
            dm = -np.min(
                [
                    np.abs(dr_min),
                    np.abs(dp_min),
                    np.abs(dl_min),
                    np.abs(dt_min),
                ]
            )

            r.append(r[-1] + dr * dm)
            p.append(p[-1] + dp * dm)
            l.append(l[-1] + dl * dm)
            t.append(t[-1] + dt * dm)
            m.append(m[-1] + dm)
            rho.append(self._rho(p[-1], t[-1]))

            if m[-1] < 0.0001 * m[0]:
                print("m went zero")
                non_zero = False
            if p[-1] < 0.0001 * p[0]:
                print("p went zero")
                non_zero = False
            if l[-1] < 0.0001 * l[0]:
                print("l went zero")
                non_zero = False
            if r[-1] < 0.0001 * r[0]:
                print("r went zero")
                non_zero = False
            if rho[-1] < 0.0001 * rho[0]:
                print("rho went zero")
                non_zero = False
            if t[-1] < 0.0001 * t[0]:
                print("t went zero")
                non_zero = False
            i += 1

        self.dict = {
            "t": np.array(t),
            "p": np.array(p),
            "r": np.array(r),
            "rho": np.array(rho),
            "l": np.array(l),
            "m": np.array(m),
            "pp1": np.array(pp1),
            "pp2": np.array(pp2),
            "pp3": np.array(pp3),
            "cno": np.array(cno),
            "F_C": np.array(fc),
            "F_R": np.array(fr),
            "nabla_s": np.array(nabla_s),
            "nabla_stable": np.array(nabla_stable),
            "epsilon": np.array(epsilon),
        }
        # print(t[-1],r[-1],rho[-1],p[-1],m[-1],l[-1],i)
        # print('congratulations you did it! ')

    def plot(self):
        T = self.dict["t"]
        P = self.dict["p"]
        r = self.dict["r"]
        L = self.dict["l"]
        M = self.dict["m"]
        rho = self.dict["rho"]
        pp1 = self.dict["pp1"]
        pp2 = self.dict["pp2"]
        pp3 = self.dict["pp3"]
        cno = self.dict["cno"]
        F_C = self.dict["F_C"]
        F_R = self.dict["F_R"]
        nabla_s = self.dict["nabla_s"]
        nabla_stable = self.dict["nabla_stable"]
        epsilon = self.dict["epsilon"]

        plt.subplot(3, 2, 1)
        plt.plot(r / r[0], T / T[0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$T/T_0$")

        plt.subplot(3, 2, 2)
        plt.plot(r / r[0], M / M[0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$M/M_0$")

        plt.subplot(3, 2, 3)
        plt.yscale("log")
        plt.plot(r / r[0], P / P[0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$P/P_0$")

        plt.subplot(3, 2, 4)
        plt.plot(r / r[0], L / L[0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$L/L_0$")

        plt.subplot(3, 2, 5)
        plt.yscale("log")
        plt.plot(r / r[0], rho / rho[0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$\\rho/\\rho_0$")
        plt.show()

        plt.xlabel("$r/r_0$")
        plt.ylabel("Fraction of energy")
        plt.plot(r / r[0], F_C / (F_C + F_R))
        plt.plot(r / r[0], F_R / (F_C + F_R))
        plt.legend(["Convection", "Radiation"])
        plt.show()

        plt.xlabel("$r/r_0$")
        plt.plot(r / r[0], pp1 / epsilon)
        plt.plot(r / r[0], pp2 / epsilon)
        plt.plot(r / r[0], pp3 / epsilon)
        plt.plot(r / r[0], cno / epsilon)
        plt.plot(r / r[0], epsilon / np.amax(epsilon))
        plt.legend(["PP1", "PP2", "PP3", "CNO", "$\epsilon/\epsilon_{max}$"])
        plt.show()

        nabla_ad = np.full(len(nabla_s), self.nabla_ad)
        plt.yscale("log")
        plt.xlabel("$r/r_0$")
        plt.xlabel("$\\nabla$")
        plt.plot(r / r0, nabla_stable)
        plt.plot(r / r0, nabla_s)
        plt.plot(r / r0, nabla_ad)
        plt.legend(["$\\nabla_{stable}$", "$\\nabla^*}$", "$\\nabla_{ad}$"])
        plt.show()

        self.cross_section(r, L, F_C)
        print(T[-1])

    def plot_r_param(self):
        l0 = 3.846e26
        m0 = 1.989e30
        r0 = 6.96e8
        t0 = 5770
        rho0 = 1.42e-7 * 1.408e3
        rr = [0.5 * r0, 0.75 * r0, r0, 1.25 * r0, 1.5 * r0]
        T = []
        P = []
        M = []
        L = []
        rho = []
        r = []

        for i in range(len(rr)):
            self.r_0 = rr[i]
            self.intergrate(0.01)
            T.append(self.dict["t"])
            P.append(self.dict["p"])
            M.append(self.dict["m"])
            L.append(self.dict["l"])
            rho.append(self.dict["rho"])
            r.append(self.dict["r"])
        print(P[0][0])
        T = np.array(T)
        P = np.array(P)
        M = np.array(M)
        L = np.array(L)
        rho = np.array(rho)
        r = np.array(r)
        # plt.suptitle('R change')
        plt.subplot(3, 2, 1)
        for i in range(len(T)):
            plt.plot(r[i] / r[i][0], T[i] / T[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$T/T_0$")

        plt.subplot(3, 2, 2)
        for i in range(len(M)):
            plt.plot(r[i] / r[i][0], M[i] / M[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$M/M_0$")

        plt.subplot(3, 2, 3)
        for i in range(len(P)):
            plt.plot(r[i] / r[i][0], P[i] / P[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$P/P_0$")

        plt.subplot(3, 2, 4)
        for i in range(len(L)):
            plt.plot(r[i] / r[i][0], L[i] / L[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$L/L_0$")

        plt.subplot(3, 2, 5)
        for i in range(len(rho)):
            plt.plot(r[i] / r[i][0], rho[i] / rho[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$\\rho/\\rho_0$")

        plt.show()

    def plot_t_param(self):
        l0 = 3.846e26
        m0 = 1.989e30
        r0 = 6.96e8
        t0 = 5770
        rho0 = 1.42e-7 * 1.408e3
        tt = [0.2 * t0, 0.5 * t0, t0, 10 * t0, 20 * t0]
        T = []
        P = []
        M = []
        L = []
        rho = []
        r = []

        for i in range(len(tt)):
            self.t_0 = tt[i]
            self.intergrate(0.01)
            T.append(self.dict["t"])
            P.append(self.dict["p"])
            M.append(self.dict["m"])
            L.append(self.dict["l"])
            rho.append(self.dict["rho"])
            r.append(self.dict["r"])

        T = np.array(T)
        P = np.array(P)
        M = np.array(M)
        L = np.array(L)
        rho = np.array(rho)
        r = np.array(r)
        plt.subplot(3, 2, 1)
        for i in range(len(T)):
            plt.plot(r[i] / r[i][0], T[i] / T[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$T/T_0$")

        plt.subplot(3, 2, 2)
        for i in range(len(M)):
            plt.plot(r[i] / r[i][0], M[i] / M[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$M/M_0$")

        plt.subplot(3, 2, 3)
        for i in range(len(P)):
            plt.plot(r[i] / r[i][0], P[i] / P[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$P/P_0$")

        plt.subplot(3, 2, 4)
        for i in range(len(L)):
            plt.plot(r[i] / r[i][0], L[i] / L[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$L/L_0$")

        plt.subplot(3, 2, 5)
        for i in range(len(rho)):
            plt.plot(r[i] / r[i][0], rho[i] / rho[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$\\rho/\\rho_0$")

        plt.show()

    def plot_rho_param(self):
        l0 = 3.846e26
        m0 = 1.989e30
        r0 = 6.96e8
        t0 = 5770
        rho0 = 1.42e-7 * 1.408e3
        rrho = [0.1 * rho0, 0.5 * rho0, rho0, 100 * rho0, 200 * rho0]
        T = []
        P = []
        M = []
        L = []
        rho = []
        r = []

        for i in range(len(rrho)):
            self.rho_0 = rrho[i]
            self.intergrate(0.01)
            T.append(self.dict["t"])
            P.append(self.dict["p"])
            M.append(self.dict["m"])
            L.append(self.dict["l"])
            rho.append(self.dict["rho"])
            r.append(self.dict["r"])

        T = np.array(T)
        P = np.array(P)
        M = np.array(M)
        L = np.array(L)
        rho = np.array(rho)
        r = np.array(r)
        # plt.suptitle('R change')
        plt.subplot(3, 2, 1)
        for i in range(len(T)):
            plt.plot(r[i] / r[i][0], T[i] / T[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$T/T_0$")

        plt.subplot(3, 2, 2)
        for i in range(len(M)):
            plt.plot(r[i] / r[i][0], M[i] / M[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$M/M_0$")

        plt.subplot(3, 2, 3)
        for i in range(len(P)):
            plt.plot(r[i] / r[i][0], P[i] / P[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$P/P_0$")

        plt.subplot(3, 2, 4)
        for i in range(len(L)):
            plt.plot(r[i] / r[i][0], L[i] / L[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$L/L_0$")

        plt.subplot(3, 2, 5)
        for i in range(len(rho)):
            plt.plot(r[i] / r[i][0], rho[i] / rho[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$\\rho/\\rho_0$")

        plt.show()

    def plot_p_param(self):
        l0 = 3.846e26
        m0 = 1.989e30
        r0 = 6.96e8
        t0 = 5770
        rho0 = 1.42e-7 * 1.408e3
        p0 = 15515
        pp = [0.5 * p0, 0.75 * p0, p0, 1.25 * p0, 1.5 * p0]
        T = []
        P = []
        M = []
        L = []
        rho = []
        r = []

        for i in range(len(pp)):
            self.P_0 = pp[i]
            self.intergrate(0.01)
            T.append(self.dict["t"])
            P.append(self.dict["p"])
            M.append(self.dict["m"])
            L.append(self.dict["l"])
            rho.append(self.dict["rho"])
            r.append(self.dict["r"])

        T = np.array(T)
        P = np.array(P)
        M = np.array(M)
        L = np.array(L)
        rho = np.array(rho)
        r = np.array(r)
        # plt.suptitle('R change')
        plt.subplot(3, 2, 1)
        for i in range(len(T)):
            plt.plot(r[i] / r[i][0], T[i] / T[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$T/T_0$")

        plt.subplot(3, 2, 2)
        for i in range(len(M)):
            plt.plot(r[i] / r[i][0], M[i] / M[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$M/M_0$")

        plt.subplot(3, 2, 3)
        for i in range(len(P)):
            plt.plot(r[i] / r[i][0], P[i] / P[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$P/P_0$")

        plt.subplot(3, 2, 4)
        for i in range(len(L)):
            plt.plot(r[i] / r[i][0], L[i] / L[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$L/L_0$")

        plt.subplot(3, 2, 5)
        for i in range(len(rho)):
            plt.plot(r[i] / r[i][0], rho[i] / rho[i][0])
        plt.xlabel("$r/r_0$")
        plt.ylabel("$\\rho/\\rho_0$")

        plt.show()

    def cross_section(self, R, L, F_C, show_every=20):
        """
        plot cross section of star
        :param R: radius, array
        :param L: luminosity, array
        :param F_C: convective flux, array
        :param show_every: plot every <show_every> steps
        """

        R_sun = 6.96e8  # [m]
        L_sun = 3.846e26  # [W]

        plt.figure(figsize=(800 / 100, 800 / 100))
        fig = plt.gcf()
        ax = plt.gca()
        r_range = 1.2 * R[0] / R_sun
        rmax = np.max(R)

        ax.set_xlim(-r_range, r_range)
        ax.set_ylim(-r_range, r_range)
        ax.set_aspect("equal")

        core_limit = 0.995 * L_sun

        j = 0
        for k in range(0, len(R) - 1):
            j += 1
            # plot every <show_every> steps
            if j % show_every == 0:
                if L[k] >= core_limit:  # outside core
                    if F_C[k] > 0.0:  # plot convection outside core
                        circle_red = plt.Circle(
                            (0, 0), R[k] / rmax, color="red", fill=False
                        )
                        ax.add_artist(circle_red)
                    else:  # plot radiation outside core
                        circle_yellow = plt.Circle(
                            (0, 0), R[k] / rmax, color="yellow", fill=False
                        )
                        ax.add_artist(circle_yellow)
                else:  # inside core
                    if F_C[k] > 0.0:  # plot convection inside core
                        circle_blue = plt.Circle(
                            (0, 0), R[k] / rmax, color="blue", fill=False
                        )
                        ax.add_artist(circle_blue)
                    else:  # plot radiation inside core
                        circle_cyan = plt.Circle(
                            (0, 0), R[k] / rmax, color="cyan", fill=False
                        )
                        ax.add_artist(circle_cyan)

        # create legends
        circle_red = plt.Circle(
            (2 * r_range, 2 * r_range), 0.1 * r_range, color="red", fill=True
        )
        circle_yellow = plt.Circle(
            (2 * r_range, 2 * r_range),
            0.1 * r_range,
            color="yellow",
            fill=True,
        )
        circle_blue = plt.Circle(
            (2 * r_range, 2 * r_range), 0.1 * r_range, color="blue", fill=True
        )
        circle_cyan = plt.Circle(
            (2 * r_range, 2 * r_range), 0.1 * r_range, color="cyan", fill=True
        )

        ax.legend(
            [circle_red, circle_yellow, circle_cyan, circle_blue],
            [
                "Convection outside core",
                "Radiation outside core",
                "Radiation inside core",
                "Convection inside core",
            ],
            fontsize=13,
        )
        plt.xlabel(r"$R$", fontsize=13)
        plt.ylabel(r"$R$", fontsize=13)
        plt.title("Cross section of star", fontsize=15)
        plt.show()

    def Sanity_check(self):
        print("Opacity table")
        print("log10(T)   log10(r)(cgs)   log10(k)(cgs)   k(SI)")
        logt = [
            3.750,
            3.755,
            3.755,
            3.755,
            3.755,
            3.770,
            3.780,
            3.795,
            3.770,
            3.775,
            3.780,
            3.795,
            3.380,
        ]
        logr = [
            -6,
            -5.95,
            -5.80,
            -5.70,
            -5.55,
            -5.95,
            -5.95,
            -5.95,
            -5.80,
            -5.75,
            -5.70,
            -5.55,
            -5.50,
        ]
        kvals = np.zeros(len(logt))
        for i in range(len(logt)):
            t = 10 ** (logt[i])
            rho = 10 ** (logr[i]) * (((t) / 1e6) ** 3) * 1e3
            kvals[i] = self.kappa_finder(10 ** (logt[i]), rho, "opacity.txt")
        logk = np.log10(kvals * 10)
        for i in range(len(logt)):
            print(
                "{:^10.3f}{:^10.2f}{:^20.2f}{:^10.2e}".format(
                    logt[i], logr[i], logk[i], kvals[i]
                )
            )

        print("\n Gradients")
        t = 0.9e6
        rho = 55.9
        r = 0.84 * 6.96e8
        m = 0.9 * 1.989e30
        l = 3.846e26
        kappa = 3.98
        p = 1e12
        g = self.G * m / (r ** 2)
        H_p = (self.N * self.kb * t) / (g)
        nabla_stable = self.nabla_stable(t, rho, r, l, kappa, H_p)
        u = self.u(t, rho, kappa, g, H_p)
        xii = self.x_i(H_p, u, self.nabla_ad, nabla_stable)
        u = self.u(t, rho, kappa, g, H_p)
        nabla_s = xii ** 2 + 2 * u / (H_p ** 2) * xii + self.nabla_ad
        v = np.sqrt(g * self.delta * (H_p ** 2) / (4 * H_p)) * xii
        fc = self.convection(t, rho, g, H_p, xii)
        fr = self.radiation(t, rho, kappa, H_p, nabla_stable, fc)

        print("H_p     = {:.1f} Mm".format(H_p / 1e6))
        print("U       = {:.2e}".format(u))
        print("xi      = {:.3e}".format(xii))
        print("Nabla_s = {:.3f}".format(nabla_s))
        print("frac_fc = {:.2f}".format(fc / (fr + fc)))
        print("frac_fr = {:.2f}".format(fr / (fr + fc)))

        print("\n Model verification")

        l0 = 3.846e26
        m0 = 1.989e30
        r0 = 6.96e8
        t0 = 5770
        rho0 = 1.42e-7 * 1.408e3
        pulsar = Star(T=t0, rho=rho0, r=r0, l=l0, m=m0)
        pulsar.intergrate(0.01)
        r = pulsar.dict["r"]
        l = pulsar.dict["l"]
        fc = pulsar.dict["F_C"]
        nabla_s = pulsar.dict["nabla_s"]
        nabla_stable = pulsar.dict["nabla_stable"]
        nabla_ad = np.full(len(nabla_s), pulsar.nabla_ad)
        plt.yscale("log")
        plt.plot(r / r0, nabla_stable)
        plt.plot(r / r0, nabla_s)
        plt.plot(r / r0, nabla_ad)
        plt.legend(["$\\nabla_{stable}$", "$\\nabla^*}$", "$\\nabla_{ad}$"])
        plt.show()

        self.cross_section(r, l, fc)


if __name__ == "__main__":

    l0 = 3.846e26
    m0 = 1.989e30
    r0 = 6.96e8
    t0 = 5770
    rho0 = 1.42e-7 * 1.408e3
    p0 = 15515
    pulsar = Star(T=t0, rho=rho0, r=r0, l=l0, m=m0)
    pulsar.intergrate(0.01)
    pulsar.plot()
# pulsar.plot_rho_param()
# pulsar.Sanity_check()
# pulsar.intergrate(0.01)
