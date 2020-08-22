from exp_decay import ExponentialDecay


def test_call():
    a = 0.4
    u = 3.2
    t = 1

    decaytest = ExponentialDecay(a)
    result = decaytest(t, u)
    assert (
        abs(abs(result) - 1.28) <= 1e-8
    ), f"The answer was something other than 1.28 the answer was =  {result}"


def test_solve():
    a = 0.4
    u = 3.2
    t = 1000
    decaytest = ExponentialDecay(a)
    y, t = decaytest.solve(u, 1, 1e-8)


if __name__ == "__main__":
    test_call()
    test_solve()
    test_call()
