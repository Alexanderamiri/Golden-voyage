import numpy as np
import matplotlib.pyplot as plt


class StellarCore:
    """A Class to calculate the energy output in the core of a star given the
    temperature and density of the star.


    Methods
    -------
    PPI
        Calculate PPI branch energy output
    PPII
        Calculate PPII branch energy output
    PPIII
        Calculate PPIII branch energy output
    CNO
        Calculates CNO cycle energy output


    Parameters
    ----------
    self.sanity : boolean
        Boolean to run Sanity check for calculated values, to enable set sanity
        == True
    self.sanity_values : dictionary
        Dictionary holding the reactions parameters for nuclear reactions
            33 : Sanity value for the helium3 helium3 reaction
            34 : Sanity value for the helium3 helium4 reaction
            e7 : Sanity value for the beryllium7 electron reaction
            m17: Sanity value for the lithium7 proton reaction
            17 : Sanity value for the beryllium7 proton reaction
            p14 : Sanity value for the nitrogen14 proton reaction
    self.temp : float
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
    self.Q_values : Dictionary
        Dictionary holding the Q values for different nuclear reactions.
        The dictionary holds the following keys:
            pp : Energy produced in the first reaction for all the PP branches
            pd : Energy produced in the second reaction for all the PP branches
            33 : Energy produced in the PPI last reaction
            34 : Energy produced in the third reaction in PPII and PPIII branch
            e7 : Energy produced in the fourth reaction in PPII branch
            m17 : Energy produced in the fifth reaction in PPII branch
            17 : Energy produced in the fourth reaction in the PPIII branch
            8 : Energy produced in the fifth reaction in the PPIII branch
            m8 : Energy produced in the sixth reaction in the PPIII branch
            p12 : Energy produced in the first reaction in the CNO cycle
            13 : Energy produced in the second reaction in the CNO cycle
            p13 : Energy produced in the third reaction in the CNO cycle
            p14 : Energy produced in the fourth reaction in the CNO cycle
            15 : Energy produced in the fifth reaction in the CNO cycle
            p15 : Energy produced in the sixth reaction in the CNO cycle
    self.lmbda.values : dictionary
        Dictionary holding the reactions parameters for nuclear reactions
            33 : Reaction parameter for the helium3 helium3 reaction
            34 : Reaction parameter for the helium3 helium4 reaction
            e7 : Reaction parameter for the beryllium7 electron reaction
            m17: Reaction parameter for the lithium7 proton reaction
            17 : Reaction parameter for the beryllium7 proton reaction
            p14 : Reaction parameter for the nitrogen14 proton reaction
    self.n_p : float
        Number for hydrogen atoms
    self.n_He : float
        Number of helium4 atoms
    self.n_He3 : float
        Number of helium3 atoms
    self.n_Li7 : float
        Number of lithium7 atoms
    self.n_Be7 : float
        Number of beryllium7 atoms
    self.n_N14 : float
        Number of nitrogen14 atoms
    """

    def __init__(self, temp, density, sanity=False):
        self.temp = temp
        self.rho = density
        self.sanity = sanity
        self.sanity_values = {
            "pp": 4.04e2,
            "33": 8.68e-9,
            "34": 4.68e-5,
            "e7": 1.47e-6,
            "m17": 5.29e-4,
            "17": 1.63e-6,
            "p14": 9.18e-8,
        }
        if self.sanity:
            self.rho = 1.62e5
            self.temp = 1.57e7
        T_9 = np.array(self.temp) / 1e9
        m_u = 1.6605e-27
        self.N_a = 6.0221e23
        self.mev_to_j = 1.6022e-13
        self.cm3_m3 = 1e-6
        self.Q_values = {
            "pp": 1.177 * self.mev_to_j,
            "pd": 5.494 * self.mev_to_j,
            "33": 12.860 * self.mev_to_j,
            "34": 1.586 * self.mev_to_j,
            "e7": 0.049 * self.mev_to_j,
            "m17": 17.346 * self.mev_to_j,
            "17": 0.137 * self.mev_to_j,
            "8": 8.367 * self.mev_to_j,
            "m8": 2.995 * self.mev_to_j,
            "p12": 1.944 * self.mev_to_j,
            "13": 1.513 * self.mev_to_j,
            "p13": 7.551 * self.mev_to_j,
            "p14": 7.297 * self.mev_to_j,
            "15": 1.757 * self.mev_to_j,
            "p15": 4.966 * self.mev_to_j,
        }
        self.lmbda_values = {
            "pp": (
                4.01e-15
                * T_9 ** (-2 / 3)
                * np.exp(-3.380 * T_9 ** (-1 / 3))
                * (
                    1
                    + 0.123 * T_9 ** (1 / 3)
                    + 1.09 * T_9 ** (2 / 3)
                    + 0.938 * T_9
                )
            )
            * self.cm3_m3
            / self.N_a,
            "33": (
                6.04e10
                * T_9 ** (-2 / 3)
                * np.exp(-12.276 * T_9 ** (-1 / 3))
                * (
                    1
                    + 0.034 * T_9 ** (1 / 3)
                    - 0.522 * T_9 ** (2 / 3)
                    - 0.124 * T_9
                    + 0.353 * T_9 ** (4 / 3)
                    + 0.213 * T_9 ** (5 / 3)
                )
            )
            * self.cm3_m3
            / self.N_a,
            "34": (
                5.61e6
                * (T_9 / (1 + 4.95e-2 * T_9)) ** (5 / 6)
                * T_9 ** (-3 / 2)
                * np.exp(-12.826 * (T_9 / (1 + 4.95e-2 * T_9)) ** (-1 / 3))
            )
            * self.cm3_m3
            / self.N_a,
            "e7": (
                1.34e-10
                * T_9 ** (-1 / 2)
                * (
                    1
                    - 0.537 * T_9 ** (1 / 3)
                    + 3.86 * T_9 ** (2 / 3)
                    + 0.0027 * T_9 ** (-1) * np.exp(2.515e-3 * T_9 ** (-1))
                )
            )
            * self.cm3_m3
            / self.N_a,
            "m17": (
                1.096e9 * T_9 ** (-2 / 3) * np.exp(-8.472 * T_9 ** (-1 / 3))
                - 4.830e8
                * (T_9 / (1 + 0.759 * T_9)) ** (5 / 6)
                * T_9 ** (-3 / 2)
                * np.exp(-8.472 * (T_9 / (1 + 0.759 * T_9)) ** (-1 / 3))
                + 1.06e10 * T_9 ** (-3 / 2) * np.exp(-30.442 * T_9 ** (-1))
            )
            * self.cm3_m3
            / self.N_a,
            "17": (
                3.11e5 * T_9 ** (-2 / 3) * np.exp(-10.262 * T_9 ** (-1 / 3))
                + 2.53e3 * T_9 ** (-3 / 2) * np.exp(-7.306 * T_9 ** (-1))
            )
            * self.cm3_m3
            / self.N_a,
            "p14": (
                4.90e7
                * T_9 ** (-2 / 3)
                * np.exp(-15.228 * T_9 ** (-1 / 3) - 0.092 * T_9 ** 2)
                * (
                    1
                    + 0.027 * T_9 ** (1 / 3)
                    - 0.778 * T_9 ** (2 / 3)
                    - 0.149 * T_9
                    + 0.261 * T_9 ** (4 / 3)
                    + 0.127 * T_9 ** (5 / 3)
                )
                + 2.37e3 * T_9 ** (-3 / 2) * np.exp(-3.011 * T_9 ** (-1))
                + 2.19e4 * np.exp(-12.53 * T_9 ** (-1))
            )
            * self.cm3_m3
            / self.N_a,
        }
        self.r_ik = None
        self.PP1_e = None
        self.PP2_e = None
        self.PP3_e = None
        self.cno_e = None
        self.X = 0.7
        self.Y_He3 = 1e-10
        self.Y = 0.29
        self.Z_Li7 = 1e-7
        self.Z_Be7 = 1e-7
        self.Z_N14 = 1e-11
        self.n_p = self.rho * self.X / m_u
        self.n_e = (1 + self.X) * self.rho / (2 * m_u)
        self.n_He = self.rho * self.Y / (4 * m_u)
        self.n_He3 = self.rho * self.Y_He3 / (3 * m_u)
        self.n_Li7 = self.rho * self.Z_Li7 / (7 * m_u)
        self.n_Be7 = self.rho * self.Z_Be7 / (7 * m_u)
        self.n_N14 = self.rho * self.Z_N14 / (14 * m_u)
        if self.sanity:
            self.Sanity_check()

    def rates(self):
        """Function to calculate reaction rates and adjust them according
         to previous reactions that has to take place first

        Parameters
        ----------
        self.r_ik : dictionary
            Dictionary holding the reactions parameters for nuclear reactions
                33 : Reaction rate for the helium3 helium3 reaction
                34 : Reaction rate for the helium3 helium4 reaction
                e7 : Reaction rate for the beryllium7 electron reaction
                m17: Reaction rate for the lithium7 proton reaction
                17 : Reaction rate for the beryllium7 proton reaction
                p14 : Reaction rate for the nitrogen14 proton reaction

        Returns
        -------
        None
        """
        self.r_ik = {
            "pp": self.n_p ** 2 * self.lmbda_values["pp"] / (2 * self.rho),
            "33": self.n_He3 ** 2 * self.lmbda_values["33"] / (2 * self.rho),
            "34": self.n_He * self.n_He3 * self.lmbda_values["34"] / self.rho,
            "e7": self.n_Be7 * self.n_e * self.lmbda_values["e7"] / self.rho,
            "m17": self.n_Li7 * self.n_p * self.lmbda_values["m17"] / self.rho,
            "17": self.n_Be7 * self.n_p * self.lmbda_values["17"] / self.rho,
            "p14": self.n_N14 * self.n_p * self.lmbda_values["p14"] / self.rho,
        }
        if np.size(self.temp) > 1:
            # Upper limit for electron capture in Be7-e reaction
            bol = np.logical_and(
                self.temp < 1e6, self.r_ik["e7"] >= 1.57e-7 / self.n_e
            )
            self.r_ik["e7"][bol] = 1.57e-7 / self.n_e

            # Reaction rate adjustment for helium3-helium3 and helium3-helium4
            bol = self.r_ik["pp"] < (2 * self.r_ik["33"] + self.r_ik["34"])
            ratio = self.r_ik["pp"][bol] / (
                2 * self.r_ik["33"][bol] + self.r_ik["34"][bol]
            )
            self.r_ik["33"][bol] *= ratio
            self.r_ik["34"][bol] *= ratio

            # Reaction rate adjustment for beryllium7-electron and lithium-P
            bol = self.r_ik["34"] < (self.r_ik["e7"] + self.r_ik["17"])
            ratio = self.r_ik["34"][bol] / (
                self.r_ik["e7"][bol] + self.r_ik["17"][bol]
            )
            self.r_ik["e7"][bol] *= ratio
            self.r_ik["17"][bol] *= ratio

            # Reaction rate adjustment for lithium7-electron
            bol = self.r_ik["e7"] < self.r_ik["m17"]
            ratio = self.r_ik["e7"][bol] / self.r_ik["m17"][bol]
            self.r_ik["m17"][bol] *= ratio

        elif np.size(self.temp) == 1:
            if self.temp < 1e6:
                self.r_ik["e7"] = 1.57e-7 / self.n_e

            if self.r_ik["pp"] < (2 * self.r_ik["33"] + self.r_ik["34"]):
                ratio = self.r_ik["pp"] / (
                    2 * self.r_ik["33"] + self.r_ik["34"]
                )
                self.r_ik["33"] *= ratio
                self.r_ik["34"] *= ratio

            if self.r_ik["34"] < (self.r_ik["e7"] + self.r_ik["17"]):
                ratio = self.r_ik["34"] / (self.r_ik["e7"] + self.r_ik["17"])
                self.r_ik["e7"] *= ratio
                self.r_ik["17"] *= ratio

            if self.r_ik["e7"] < self.r_ik["m17"]:
                ratio = self.r_ik["e7"] / self.r_ik["m17"]
                self.r_ik["m17"] *= ratio

    def Sanity_check(self):
        """Function to perform sanity check on reaction rates

        Prints
        ------
            r_ik * Q_ik * rho for each reaction rate



        Returns
        -------
        None
        """
        self.rates()
        calculated = {
            "pp": self.r_ik["pp"]
            * (self.Q_values["pp"] + self.Q_values["pd"])
            * self.rho,
            "33": self.r_ik["33"] * self.Q_values["33"] * self.rho,
            "34": self.r_ik["34"] * self.Q_values["34"] * self.rho,
            "e7": self.r_ik["e7"] * self.Q_values["e7"] * self.rho,
            "m17": self.r_ik["m17"] * self.Q_values["m17"] * self.rho,
            "17": self.r_ik["17"]
            * (self.Q_values["17"] + self.Q_values["8"] + self.Q_values["m8"])
            * self.rho,
            "p14": self.r_ik["p14"]
            * (
                self.Q_values["p12"]
                + self.Q_values["p13"]
                + self.Q_values["13"]
                + self.Q_values["p15"]
                + self.Q_values["15"]
                + self.Q_values["p14"]
            )
            * self.rho,
        }
        for calc, san in zip(calculated, self.sanity_values):
            a = calculated[calc]
            b = self.sanity_values[san]
            check = (1 - 1e-1) < abs(a / b) < (1 + 1e-1)
            print(
                "{:5s}| Calculated = {:9.2e} | Sanity = {:9.2e}"
                " | Sanity check returned {:5s}".format(calc, a, b, str(check))
            )

    def PPI(self):
        """This function will calculate the energy output of the PPI branch
        where the following reaction occurs
        H1 + H1 > D2 + e + mu + Q
        D2 + H1 > He3 + Q
        He3 + He3 > He4 + 2*H1 + Q

        Parameters
        ----------
        self.PP1_e : np.array
            Energy output of PPI branch as function of temperature

        Returns
        -------
        None
        """
        self.PP1_e = self.r_ik["33"] * (
            self.Q_values["pp"] + self.Q_values["pd"] + self.Q_values["33"]
        )
        return self.PP1_e

    def PPII(self):
        """This function will calculate the energy output of the PPII branch
        where the following reaction occurs
        H1 + H1 > D2 + e + mu + Q
        D2 + H1 > He3 + Q
        He3 + He4 > Be7 + Q
        Be7 + e > Li7 + mu + delE
        Li7 + H1 > 2*He4 + Q

        Parameters
        ----------
        self.PP2_e : np.array
            Energy output of PPII branch as function of temperature

        Returns
        -------
        None
        """
        self.PP2_e = (
            self.r_ik["34"]
            * (self.Q_values["34"] + self.Q_values["pp"] + self.Q_values["pd"])
            + self.r_ik["e7"] * self.Q_values["e7"]
            + self.r_ik["m17"] * self.Q_values["m17"]
        )
        return self.PP2_e

    def PPIII(self):
        """This function will calculate the energy output of the PPIII branch
        where the following reaction occurs
        H1 + H1 > D2 + e + mu + Q
        D2 + H1 > He3 + Q
        He3 + He4 > Be7 + Q
        Be7 + H1 > B8 + Q
        B8 > Be8 + e + mu + Q
        Be8 > 2* He4 + Q

        Parameters
        ----------
        self.PP3_e : np.array
            Energy output of PPIII branch as function of temperature

        Returns
        -------
        None
        """
        self.PP3_e = self.r_ik["34"] * (
            self.Q_values["34"] + self.Q_values["pp"] + self.Q_values["pd"]
        ) + self.r_ik["17"] * (
            self.Q_values["17"] + self.Q_values["8"] + self.Q_values["m8"]
        )
        return self.PP3_e

    def CNO(self):
        """This function will calculate the energy output of the CNO cycle
        where the following reaction occurs
        C12 + H1 > N13 + Q
        N13 > C13 + ep + mu + Q
        C13 + H1 > N14 + Q
        N14 + H1 > O15 + Q
        O15 > N15 + ep + mu + Q
        N15 + H1 > C12 + He4 + Q

        Parameters
        ----------
        self.cno_e : np.array
            Energy output of CNO cycle as function of temperature

        Returns
        -------
        None
        """
        self.cno_e = self.r_ik["p14"] * (
            self.Q_values["p12"]
            + self.Q_values["13"]
            + self.Q_values["p13"]
            + self.Q_values["p14"]
            + self.Q_values["15"]
            + self.Q_values["p15"]
        )
        return self.cno_e

    def epsilon(self):
        self.rates()
        self.e = (
            self.r_ik["pp"] * self.Q_values["pp"]
            + self.r_ik["33"] * self.Q_values["33"]
            + self.r_ik["34"] * self.Q_values["34"]
            + self.r_ik["e7"] * self.Q_values["e7"]
            + self.r_ik["m17"] * self.Q_values["m17"]
            + self.r_ik["17"] * self.Q_values["17"]
            + self.r_ik["p14"] * self.Q_values["p14"]
        )
        return self.e

    def plot(self):
        """Plots the different energy outputs of all PP branches as well
         as the CNO cycle and the relative energy outputs normalized over PPI


        Returns
        -------
        None
        """
        self.rates()
        self.PPI()
        self.PPII()
        self.PPIII()
        self.CNO()
        plt.figure()
        plt.yscale("log")
        plt.xscale("log")
        plt.plot(self.temp, self.PP1_e)
        plt.plot(self.temp, self.PP2_e)
        plt.plot(self.temp, self.PP3_e)
        plt.plot(self.temp, self.cno_e)

        plt.xlabel("Temperature [K]")
        plt.ylabel("Energy [$ J \  m^3 \ s^{-1} \ kg^{-1} $]")
        plt.title("Energy production rate")
        plt.legend(["PPI", "PPII", "PPIII", "CNO"], loc="lower right")
        plt.show()

        plt.figure(dpi=900)
        plt.xscale("log")
        plt.yscale("log")
        plt.plot(self.temp, self.PP1_e / self.PP1_e)
        plt.plot(self.temp, self.PP2_e / self.PP1_e)
        plt.plot(self.temp, self.PP3_e / self.PP1_e)
        plt.plot(self.temp, self.cno_e / self.PP1_e)
        plt.xlabel("Temperature [K]")
        plt.ylabel("Energy / PP1 [$ J \  m^3 \ s^{-1} \ kg^{-1} $]")
        plt.title("Relative Energy production rate [Norm. over PPI]")
        plt.legend(["PPI", "PPII", "PPIII", "CNO"], loc="lower right")
        plt.show()


if __name__ == "__main__":
    sun_density = 1.62e5
    sun_temp = 1.57e7
    t = np.linspace(1e4, 1e9, 1000000)
    k = np.array([sun_temp, 1.8e7])
    sun = StellarCore(temp=t, density=sun_density, sanity=True)
    sun.plot()
