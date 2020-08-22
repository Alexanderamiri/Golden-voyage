import numpy as np


def eta_finder(mu, b, sigma, n):
    """Finds eta given mu, sigma, n and B

    Parameters
    ----------
    mu : float
        mean value
    b : float
        Steps
    sigma : float
        Standard deviation
    n : int
        Sum steps

    Returns
    -------
    np.array
    """
    M = np.zeros(b)
    N = np.zeros(b)
    for i in range(b):
        y = np.random.normal(mu, sigma, n)
        y_avg = np.mean(y)
        s = np.sum((y - y_avg) ** 2 / (n - 1))
        M[i] = np.exp(y_avg)
        N[i] = np.exp(y_avg - s / (2 * n))
    return M, N


n_0 = [10, 30]
mu_0 = 0.7
B_0 = 10000
sigma_0 = 1.2

eta_s_10, eta_hat_10 = eta_finder(mu_0, B_0, sigma_0, n_0[0])
eta_s_mu_10 = np.mean(eta_s_10)
eta_s_sigma_10 = np.std(eta_s_10)
eta_hat_mu_10 = np.mean(eta_hat_10)
eta_hat_sigma_10 = np.std(eta_hat_10)

eta_s_30, eta_hat_30 = eta_finder(mu_0, B_0, sigma_0, n_0[1])
eta_s_mu_30 = np.mean(eta_s_30)
eta_s_sigma_30 = np.std(eta_s_30)
eta_hat_mu_30 = np.mean(eta_hat_30)
eta_hat_sigma_30 = np.std(eta_hat_30)

print(
    "For n = 10 \neta* : mu = {:.3f}, sigma = {:.3f}"
    "\neta_hat : mu = {:.3f}, sigma = {:.3f}".format(
        eta_s_mu_10, eta_s_sigma_10, eta_hat_mu_10, eta_hat_sigma_10
    )
)
print(
    "\nFor n = 30 \neta* : mu = {:.3f}, sigma = {:.3f}"
    "\neta_hat : mu = {:.3f}, sigma = {:.3f}".format(
        eta_s_mu_30, eta_s_sigma_30, eta_hat_mu_30, eta_hat_sigma_30
    )
)

"""

For n = 10 
eta* : mu = 2.159, sigma = 0.840
eta_hat : mu = 2.011, sigma = 0.786

For n = 30 
eta* : mu = 2.070, sigma = 0.462
eta_hat : mu = 2.021, sigma = 0.451

"""
