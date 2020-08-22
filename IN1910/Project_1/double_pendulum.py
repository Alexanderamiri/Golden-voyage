from numpy import sin, cos, pi, gradient
from scipy import integrate
from matplotlib.pyplot import plot, show, figure, axis, rcParams
from matplotlib.animation import FuncAnimation, FFMpegWriter

rcParams["animation.ffmpeg_path"] = "C:/FFmpeg/bin/ffmpeg.exe"


class DoublePendulum:
    def __init__(self, m1, l1, m2, l2):
        self.M1 = m1
        self.M2 = m2
        self.L1 = l1
        self.L2 = l2
        self.g = 9.81

    def __call__(self, t, u):
        theta1 = u[1]
        a = self.M2 * self.L1 * u[1] ** 2 * sin(u[2] - u[0]) * cos(u[2] - u[0])
        b = self.M2 * self.g * sin(u[2]) * cos(u[2] - u[0])
        c = self.M2 * self.L2 * u[3] ** 2 * sin(u[2] - u[0])
        d = (self.M1 + self.M2) * self.g * sin(u[0])
        e = (self.M1 + self.M2) * self.L1
        f = -self.M2 * self.L1 * cos(u[2] - u[0]) ** 2
        omega1 = (a + b + c - d) / (e + f)

        omega2 = (
            -self.M2
            * self.L2
            * u[3] ** 2
            * sin(u[2] - u[0])
            * cos(u[2] - u[0])
            + (self.M1 + self.M2) * self.g * sin(u[0]) * cos(u[2] - u[0])
            - (self.M1 + self.M2) * self.L1 * u[1] ** 2 * sin(u[2] - u[0])
            - (self.M1 + self.M2) * self.g * sin(u[2])
        ) / (
            (self.M1 + self.M2) * self.L2
            - self.M2 * self.L2 * cos(u[2] - u[0]) ** 2
        )
        theta2 = u[3]
        return theta1, omega1, theta2, omega2

    def solve(self, u, T, dt, angles="rad"):
        if angles == "deg":
            u[0] *= 180 / pi
            u[2] *= 180 / pi
        p = integrate.solve_ivp(
            self.__call__,
            (0, T),
            u,
            method="Radau",
            dense_output=True,
            max_step=dt,
        )
        self.dt = dt
        self._t = p.t
        self._theta1 = p.y[0]
        self._theta2 = p.y[2]
        self._x1 = self.L1 * sin(self._theta1)
        self._y1 = -self.L1 * cos(self._theta1)
        self._x2 = self._x1 + self.L2 * sin(self.theta2)
        self._y2 = self._y1 - self.L2 * cos(self._theta2)
        self._vx1 = gradient(self._x1, self._t)
        self._vy1 = gradient(self._y1, self._t)
        self._vx2 = gradient(self._x2, self._t)
        self._vy2 = gradient(self._y2, self._t)
        self.p1 = self.M1 * self.g * (self._y1 + self.L1)
        self.p2 = self.M2 * self.g * (self._y2 + self.L1 + self.L2)
        self.k1 = 0.5 * self.M1 * (self._vx1 ** 2 + self._vy1 ** 2)
        self.k2 = 0.5 * self.M2 * (self._vx2 ** 2 + self._vy2 ** 2)
        self._potential = self.p1 + self.p2
        self._kinetic = self.k1 + self.k2
        return p.t, p.y[0], p.y[1], p.y[2], p.y[3]

    def _next_frame(self, i):
        self.pendulums.set_data(
            (0, self.x1[i], self.x2[i]), (0, self.y1[i], self.y2[i])
        )
        return (self.pendulums,)

    def create_animation(self):
        fig = figure()
        axis("equal")
        axis("off")
        axis((-3, 3, -3, 3))
        (self.pendulums,) = plot([], [], "o-", lw=2)
        self.animation = FuncAnimation(
            fig, self._next_frame, frames=600, interval=16, blit=True
        )

    def show_animation(self):
        self.create_animation()
        show()

    def save_animation(self, name):
        self.create_animation()
        ffwriter = FFMpegWriter(fps=60)
        self.animation.save(name, writer=ffwriter)

    @property
    def t(self):
        if hasattr(self, "_t"):
            return self._t
        else:
            return None

    @property
    def theta1(self):
        if hasattr(self, "_theta1"):
            return self._theta1
        else:

            return None

    @property
    def theta2(self):
        if hasattr(self, "_theta2"):
            return self._theta2
        else:

            return None

    @property
    def x1(self):
        if hasattr(self, "_x1"):
            return self._x1
        else:

            return None

    @property
    def y1(self):
        if hasattr(self, "_y1"):
            return self._y1
        else:
            return None

    @property
    def x2(self):
        if hasattr(self, "_x2"):
            return self._x2
        else:
            return None

    @property
    def y2(self):
        if hasattr(self, "_y2"):
            return self._y2
        else:
            return None

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
    def vx1(self):
        if hasattr(self, "_vx1"):
            return self._vx1
        else:
            return None

    @property
    def vy1(self):
        if hasattr(self, "_vy1"):
            return self._vy1
        else:
            return None

    @property
    def vx2(self):
        if hasattr(self, "_vx2"):
            return self._vx2
        else:
            return None

    @property
    def vy2(self):
        if hasattr(self, "_vy2"):
            return self._vy2
        else:
            return None


if __name__ == "__main__":
    scenario = DoublePendulum(2, 1, 2, 1)
    u = [pi / 2, 0, pi, 0]
    t, theta1, omega1, theta2, omega2 = scenario.solve(u, 10, 1e-2)
    scenario.save_animation("pendulumss.mp4")
