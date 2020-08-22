from numpy import mean, linspace, zeros
from pendulum import Pendulum


def test_solve():
    L = 2.7
    omega = 0
    theta = 0
    scenario = Pendulum(L)
    x, omega1, theta1, x, y = scenario.solve([omega, theta], 10, 1e-10)
    assert mean(omega1) <= 1e-6, (
        f"Mean Omega is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {omega1}"
    )
    assert mean(theta1) <= 1e-6, (
        f"Mean Theta is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {theta1}"
    )
    x1, omega2, theta2, x, y = scenario.solve([omega, theta], 10, 1e-10, "deg")
    assert mean(theta2) <= 1e-6, (
        f"Mean Omega is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {theta2}"
    )
    assert mean(omega2) <= 1e-6, (
        f"Mean Theta is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {omega2}"
    )


def test_properties():
    scenario = Pendulum(10)
    assert scenario.t == None, "solve() not called but t still had a value"
    assert (
        scenario.theta == None
    ), "solve() not called but theta still had a value"
    assert (
        scenario.omega == None
    ), "solve() not called but omega still had a value"


def test_properties_zeros():
    L = 2.7
    omega = 0
    theta = 0
    scenario = Pendulum(L)
    t, omega, theta, x, y = scenario.solve([omega, theta], 10, 1e-3)
    tt = linspace(0, 10, 10004)
    zeroo = zeros(len(omega))
    assert L ** 2 - (mean(x) ** 2 + mean(y) ** 2) < 1e-6
    assert mean(omega) == mean(
        zeroo
    ), "omega set to zeros did not yield zeros array"
    assert mean(theta) == mean(
        zeroo
    ), "theta set to zeros did not yield zeros array"
    assert (
        abs(mean(t) - mean(tt)) < 1e-2
    ), "t was not equal to linspace(0,T,dt)"


if __name__ == "__main__":
    test_solve()
    test_properties()
    test_properties_zeros()
