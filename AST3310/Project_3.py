import fvis3
import numpy as np


class Convection2D:
    def __init__(self, Gaussian_perturbation=False):
        """Class to simulate 2 dimensional convection in a star.

        Methods
        -------
        initialise()
            Initializes temperature, pressure, density and internal energy
        time_step()
            Calculates the time step
        boundary_conditions()
            Boundary conditions for energy, density and velocity
        central_x(func)
            Central difference scheme in x-direction
        central_y(func)
            Central difference scheme in y-direction
        upwind_x(func, u)
            Upwind difference scheme in y-direction
        upwind_y(func, u)
            Upwind difference scheme in y-direction
        hydro_solver()
            Hydrodynamic equations solver

        Parameters
        ----------
        self.Gaussian_perturbation : boolean
            Gaussian perturbation for instability
        self.kb : float
            Boltzmann constant
        self.m_u : float
            Atomic mass
        self.mu : float
            Mean molecular weight
        self.G : float
            Gravitational constant
        self.t_sun : int
            Temperature of the sun
        self.m_sun : float
            Mass of the sun
        self.r_sun : float
            Radius of the sun
        self.p_sun : float
            Pressure of the sun
        self.nabla : float
            Temperature Gradient
        self.Y : float
            Heat ratio
        self.p : float
            Numerical constant
        self.rho_sun : float
            Density of the sun
        self.g : float
            Gravity acceleration
        self.e_sun
            Energy density
        self.x_max : float
            Number of x points
        self.y_max : float
            Number of x points
        self.nx : float
            Size in the x direction
        self.ny : float
            Size in the y direction
        self.x : np.array
            x points
        self.y : np.array
            y points
        self.dx : float
            Difference in x
        self.dy : float
            Difference in y
        self.u0 : float
            Initial flow in x direction
        self.w0 : float
            Initial flow in y direction
        self.T : np.array
            Array containing temperature
        self.P : np.array
            Array containing pressure
        self.u : np.array
            Array containing x flow
        self.w : np.array
            Array containing y flow
        self.e : np.array
            Array containing energy densities
        self.rho: np.array
            Array containing density
        """
        self.Gaussian_perturbation = Gaussian_perturbation
        self.mu = 0.61
        self.m_u = 1.6605e-27
        self.G = 6.67408e-11
        self.Y = 5.0 / 3
        self.kb = 1.38064852e-23
        self.p = 0.1
        self.m_sun = 1.989e30
        self.r_sun = 6.96e8
        self.g = -6.67408e-11 * (1.989e30) / (6.96e8) ** 2
        self.nabla = 2 / 5 * 1.1
        self.p_sun = 1.8e8
        self.t_sun = 5770
        self.e_sun = self.p_sun / (self.Y - 1)
        self.rho_sun = self.p_sun * self.mu * self.m_u / (self.kb * self.t_sun)

        self.nx = 300
        self.ny = 100
        self.x_max = 12e6
        self.y_max = 4e6
        self.x = np.linspace(0, self.x_max, self.nx)
        self.dx = self.x[1] - self.x[0]
        self.y = np.linspace(0, self.y_max, self.ny)
        self.dy = self.y[1] - self.y[0]

        self.rho = np.zeros((self.ny, self.nx))
        self.e = np.zeros((self.ny, self.nx))
        self.u = np.zeros((self.ny, self.nx))
        self.w = np.zeros((self.ny, self.nx))
        self.P = np.zeros((self.ny, self.nx))
        self.T = np.zeros((self.ny, self.nx))

    def initialise(self):
        """Initialise temperature, pressure, density and internal energy"""
        for i in range(self.nx):
            self.T[:, i] = (
                self.t_sun
                + self.mu
                * self.m_u
                * self.nabla
                * self.g
                * (self.y - self.y_max)
                / self.kb
            )
        self.P = self.p_sun * (self.T / self.t_sun) ** (1 / self.nabla)

        if self.Gaussian_perturbation:
            x_mean = 6e6
            y_mean = 2e6
            sigma = 8e5
            xx, yy = np.meshgrid(self.x, self.y)
            gaussian = self.t_sun * np.exp(
                -((xx - x_mean) ** 2 + (yy - y_mean) ** 2) / (2 * sigma ** 2)
            )
            self.T[:, :] = self.T[:, :] + gaussian

        self.rho[:, :] = self.P * self.mu * self.m_u / (self.kb * self.T[:, :])
        self.e[:, :] = self.P[:, :] / (self.Y - 1)

    def time_step(self):
        """Calculates the time step"""

        rho_rel = np.abs(self.rho_dt / self.rho)
        rho_rel_max = np.max(rho_rel)
        e_rel = np.abs(self.e_dt / self.e)
        e_rel_max = np.max(e_rel)
        x_rel = np.abs(self.u / self.dx)
        x_rel_max = np.max(x_rel)
        y_rel = np.abs(self.w / self.dy)
        y_rel_max = np.max(y_rel)
        rel = [rho_rel_max, e_rel_max, x_rel_max, y_rel_max]
        delta = np.max(np.abs(rel))

        if 0.1 <= delta <= 1e3:
            self.dt = self.p / delta
        else:
            self.dt = self.p

    def boundary_conditions(self):
        """Boundary conditions for energy, density and velocity"""
        ce = 2 * self.dy * self.g * self.mu * self.m_u / self.kb
        self.e[0, :] = (4 * self.e[1, :] - self.e[2, :]) / (
            ce / self.T[0, :] + 3
        )
        self.rho[0, :] = (
            self.e[0, :]
            * (self.Y - 1)
            * self.mu
            * self.m_u
            / (self.kb * self.T[0, :])
        )
        self.u[0, :] = (4 * self.u[1, :] - self.u[2, :]) / 3
        self.w[0, :] = 0

        self.e[-1, :] = (4 * self.e[-2, :] - self.e[-3, :]) / (
            3 - ce / self.T[-1, :]
        )
        self.rho[-1, :] = (
            self.e[-1, :]
            * (self.Y - 1)
            * self.mu
            * self.m_u
            / (self.kb * self.T[-1, :])
        )
        self.u[-1, :] = (4 * self.u[-2, :] - self.u[-3, :]) / 3
        self.w[-1, :] = 0

    def central_x(self, func):
        """Central difference scheme in x-direction

        Parameters
        ----------
        func : np.array
            Function to be differentiate

        Returns
        -------
        np.array
            Central differentiated function in x-direction"""

        roll_left = np.roll(func, -1, axis=1)
        roll_right = np.roll(func, 1, axis=1)
        f_dx = (roll_left - roll_right) / (2 * self.dx)
        return f_dx

    def central_y(self, func):
        """Central difference scheme in y-direction

        Parameters
        ----------
        func : np.array
            Function to be differentiate

        Returns
        -------
        np.array
            Central differentiated function in y-direction"""
        roll_up = np.roll(func, -1, axis=0)
        roll_down = np.roll(func, 1, axis=0)
        f_dy = (roll_up - roll_down) / (2 * self.dy)
        return f_dy

    def upwind_x(self, func, u):
        """Upwind difference scheme in x-direction

        Parameters
        ----------
        func : np.array
            Function to be differentiate
        u : np.array
            Variable function is dependant on

        Returns
        -------
        np.array
            Upwind differentiated function in x-direction"""
        f_dx = np.zeros_like(func)
        roll_left = np.roll(func, -1, axis=1)
        roll_right = np.roll(func, 1, axis=1)
        f1 = (func - roll_right) / self.dx
        f2 = (roll_left - func) / self.dx
        f_dx[np.where(u >= 0)] = f1[np.where(u >= 0)]
        f_dx[np.where(u < 0)] = f2[np.where(u < 0)]
        return f_dx

    def upwind_y(self, func, u):
        """Upwind difference scheme in y-direction

        Parameters
        ----------
        func : np.array
            Function to be differentiate
        u : np.array
            Variable function is dependant on

        Returns
        -------
        np.array
            Upwind differentiated function in y-direction"""
        f_dy = np.zeros_like(func)
        roll_up = np.roll(func, -1, axis=0)
        roll_down = np.roll(func, 1, axis=0)
        f1 = (func - roll_down) / self.dy
        f2 = (roll_up - func) / self.dy
        f_dy[np.where(u >= 0)] = f1[np.where(u >= 0)]
        f_dy[np.where(u < 0)] = f2[np.where(u < 0)]
        return f_dy

    def hydro_solver(self):
        """Hydrodynamic equations solver

        Returns
        -------
        float
            delta t
        """
        u_dx = self.central_x(self.u)
        w_dy = self.central_y(self.w)
        P_dx = self.central_x(self.P)
        P_dy = self.central_y(self.P)

        rho_dx_upwind = self.upwind_x(self.rho, self.u)
        rho_dy_upwwind = self.upwind_y(self.rho, self.w)
        rho_udx_upwind = self.upwind_x(self.rho * self.u, self.u)
        rho_udy_upwind = self.upwind_y(self.rho * self.u, self.w)
        rho_wdx_upwind = self.upwind_x(self.rho * self.w, self.u)
        rho_wdy_upwind = self.upwind_y(self.rho * self.w, self.w)
        u_dx_uu = self.upwind_x(self.u, self.u)
        u_dx_uw = self.upwind_x(self.u, self.w)
        w_dy_uu = self.upwind_y(self.w, self.u)
        w_dy_uw = self.upwind_y(self.w, self.w)
        e_dx = self.upwind_x(self.e, self.u)
        e_dy = self.upwind_y(self.e, self.w)

        self.rho_dt = (
            -self.rho * (u_dx + w_dy)
            - self.u * rho_dx_upwind
            - self.w * rho_dy_upwwind
        )
        self.e_dt = (
            -(self.e + self.P) * (u_dx + w_dy) - self.u * e_dx - self.w * e_dy
        )
        self.rho_udt = (
            -self.rho * self.u * (u_dx_uu + w_dy_uu)
            - self.u * rho_udx_upwind
            - self.w * rho_udy_upwind
            - P_dx
        )
        self.rho_wdt = (
            -self.rho * self.w * (u_dx_uw + w_dy_uw)
            - self.u * rho_wdx_upwind
            - self.w * rho_wdy_upwind
            - P_dy
            + self.rho * self.g
        )

        self.time_step()
        rho_previous = np.zeros_like(self.rho)
        rho_previous[:, :] = self.rho
        self.rho[:, :] = self.rho + self.rho_dt * self.dt
        self.e[:, :] = self.e + self.e_dt * self.dt
        self.u[:, :] = (
            rho_previous * self.u + self.rho_udt * self.dt
        ) / self.rho
        self.w[:, :] = (
            rho_previous * self.w + self.rho_wdt * self.dt
        ) / self.rho

        self.boundary_conditions()
        self.T[:, :] = (
            (self.Y - 1) * self.e * self.mu * self.m_u / (self.kb * self.rho)
        )
        self.P[:, :] = (self.Y - 1) * self.e
        uw = (self.u, self.w)
        v = np.linalg.norm(uw)
        dt = self.dt

        return dt


if __name__ == "__main__":
    convec = Convection2D(Gaussian_perturbation=False)
    convec.initialise()
    animation = fvis3.FluidVisualiser()
    animation.save_data(
        180,
        convec.hydro_solver,
        rho=convec.rho,
        e=convec.e,
        u=convec.u,
        w=convec.w,
        P=convec.P,
        T=convec.T,
        sim_fps=1.0,
    )
    animation.animate_2D(
        "ev",
        title="Convection in 2 dimension",
        anim_time=180,
        save=True,
        video_fps=10,
    )
