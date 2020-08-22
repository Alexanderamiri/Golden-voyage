from numpy import sin, pi, cos, gradient
from scipy import integrate
from matplotlib.pyplot import plot, show, legend


class Pendulum:
    def __init__(self, L=1.0, M=1.0):
        self.L = L
        self.M = M
        self.gravity = 9.81

    def __call__(self, t, u):
        return u[1], -(self.gravity / self.L) * sin(u[0])

    def solve(self, u, T, dt, angles="rad"):
        if angles == "deg":
            u[1] *= 180 / pi
        p = integrate.solve_ivp(
            self.__call__,
            (0, T),
            u,
            method="RK45",
            dense_output=True,
            first_step=dt,
            max_step=1e-2,
        )

        self._t = p.t
        self._theta = p.y[1]
        self._omega = p.y[0]
        self._x = self.L * sin(self._theta)
        self._y = -self.L * cos(self._theta)
        self._vx = gradient(self._x, self._t)
        self._vy = gradient(self._y, self._t)
        self._potential = self.M * self.gravity * (self._y + self.L)
        self._kinetic = 0.5 * self.M * (self._vx ** 2 + self._vy ** 2)
        return p.t, p.y[0], p.y[1], self._x, self._y

    @property
    def t(self):
        if hasattr(self, "_t"):
            return self._t
        else:
            return None

    @property
    def theta(self):
        if hasattr(self, "_theta"):
            return self._theta
        else:
            None

    @property
    def omega(self):
        if hasattr(self, "_omega"):
            return self._omega
        else:
            None

    @property
    def x(self):
        if hasattr(self, "_x"):
            return self._x
        else:
            None

    @property
    def y(self):
        if hasattr(self, "_y"):
            return self._y
        else:
            None

    @property
    def potential(self):
        if hasattr(self, "_potential"):
            return self._potential
        else:
            return None

    @property
    def kinetic(self):
        if hasattr(self, "_kinetic"):
            return self._kinetic
        else:
            return None

    @property
    def vx(self):
        if hasattr(self, "_vx"):
            return self._vx
        else:
            return None

    @property
    def vy(self):
        if hasattr(self, "_vy"):
            return self._vy
        else:
            return None


class DampenedPendulum(Pendulum):
    def __init__(self, L, M, B=1.0):
        Pendulum.__init__(self, L, M)
        self.B = B

    def __call__(self, t, u):
        return (
            u[1],
            -(self.gravity / self.L) * sin(u[0]) - self.B / self.M * u[1],
        )


if __name__ == "__main__":
    scenario = Pendulum(2.7, 2)
    scenario2 = DampenedPendulum(2.7, 2, 1)
    omeg = 0.15
    tht = pi / 6
    t, omega, theta, x, y = scenario.solve([omeg, tht], 10, 1e-10)
    t2, omega2, theta2, x2, y2 = scenario2.solve([omeg, tht], 10, 1e-10)
    plot(t, theta)
    plot(t, scenario.kinetic)
    plot(t, scenario.potential)
    plot(t, (scenario.kinetic + scenario.potential))
    plot(t, (scenario2.kinetic + scenario2.potential))
    legend(["theta", "kinetic", "potential", "totalenergy", "2"])
    show()
