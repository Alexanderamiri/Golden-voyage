from numpy import mean, linspace, zeros
from double_pendulum import DoublePendulum
from nose.tools import assert_equal


def test_solve():
    u = [0, 0, 0, 0]
    scenario = DoublePendulum(1, 1, 1, 1)
    t, theta1, omega1, theta2, omega2 = scenario.solve(u, 10, 1e-3)
    assert mean(theta1) <= 1e-6, (
        f"Mean Theta is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {theta1}"
    )
    assert mean(omega1) <= 1e-6, (
        f"Mean Omega is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {omega1}"
    )
    assert mean(theta2) <= 1e-6, (
        f"Mean Theta is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {theta2}"
    )
    assert mean(omega2) <= 1e-6, (
        f"Mean Omega is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {omega2}"
    )
    t, theta1, omega1, theta2, omega2 = scenario.solve(u, 10, 1e-3, "deg")
    assert mean(theta1) <= 1e-6, (
        f"Mean Theta is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {theta1}"
    )
    assert mean(omega1) <= 1e-6, (
        f"Mean Omega is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {omega1}"
    )
    assert mean(theta2) <= 1e-6, (
        f"Mean Theta is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {theta2}"
    )
    assert mean(omega2) <= 1e-6, (
        f"Mean Omega is not zero when start values for Omega and Theta is zero"
        f", Mean Omega is {omega2}"
    )


def test_properties():
    scenario = DoublePendulum(1, 1, 1, 1)
    assert_equal(
        scenario.t, None
    ), "solve() not called but t still had a value"
    assert_equal(
        scenario.theta1, None
    ), "solve() not called but theta still had a value"
    assert_equal(
        scenario.theta2, None
    ), "solve() not called but omega still had a value"


def test_properties_zeros():
    scenario = DoublePendulum(1, 1, 1, 1)
    t, theta1, omega1, theta2, omega2 = scenario.solve([0, 0, 0, 0], 10, 1e-3)
    tt = linspace(0, 10, 10004)
    zeroo = zeros(len(theta1))
    assert mean(theta1) == mean(
        zeroo
    ), "theta1 set to zeros did not yield zeros array"
    assert mean(theta2) == mean(
        zeroo
    ), "theta2 set to zeros did not yield zeros array"
    assert (
        abs(mean(t) - mean(tt)) < 1e-2
    ), "t was not equal to linspace(0,T,dt)"


if __name__ == "__main__":
    test_solve()
    test_properties()
    test_properties_zeros()
