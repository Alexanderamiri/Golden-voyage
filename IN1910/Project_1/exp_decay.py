from scipy import integrate


class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, t, u):
        return -self.a * u

    def solve(self, u0, T, dt):
        p = integrate.solve_ivp(self.__call__, [0, T], [u0])
        return p.y, p.t
