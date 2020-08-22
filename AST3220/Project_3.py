import numpy as np
import matplotlib.pyplot as plt

hbar = 1.054571817e-34
G = 6.674
c = 299792458
n = 1000000
E_P_2 = hbar * c ** 5 / G
phi_i = 11 * np.sqrt(E_P_2) / (2 * np.sqrt(np.pi))


def V(x):
    return x ** 2 * E_P_2 / (2 * 1e4 * (hbar * c) ** 3)


def small_v(x):
    return x ** 2 * E_P_2 / (2 * 1e4 * (H_i * hbar) ** 2)


def dv_dpsi(x):
    return x * E_P_2 / (1e4 * (H_i * hbar) ** 2)


def psi_conv(phi):
    return phi / np.sqrt(E_P_2)


def phi_slow_roll(t):
    return phi_i - t * E_P_2 / (hbar * np.sqrt(12 * np.pi) * 1e2)


T = 250
tau = np.linspace(0, T, n)
psi = np.zeros(n)
hsqr = np.zeros(n)
psi = np.zeros(n)
p = np.zeros(n)
h_vals = np.zeros(n)

H_i = np.sqrt(8 * np.pi * G * V(phi_i) / (3 * c ** 2))
psi[0] = psi_conv(phi_i)
dot_psi = -dv_dpsi(psi[0]) / 3
p[0] = (0.5 * dot_psi ** 2 - small_v(psi_conv(phi_i))) / (
    0.5 * dot_psi ** 2 + small_v(psi_conv(phi_i))
)
hsqr[0] = 1
dt = T / n

for i in range(n - 1):
    a = -3 * hsqr[i] * dot_psi - dv_dpsi(psi[i])
    dot_psi = dot_psi + a * dt
    psi[i + 1] = psi[i] + dot_psi * dt
    hsqr[i + 1] = np.sqrt(
        np.abs(8 * np.pi / 3 * (0.5 * dot_psi ** 2 + small_v(psi[i + 1])))
    )
    h_vals[i + 1] = h_vals[i] + hsqr[i + 1] * dt
    p[i + 1] = (0.5 * dot_psi ** 2 - small_v(psi[i + 1])) / (
        0.5 * dot_psi ** 2 + small_v(psi[i + 1])
    )

plt.plot(tau, psi)
plt.plot(tau, psi_conv(phi_slow_roll(tau / H_i)))
plt.xlabel("Time $\\tau$")
plt.ylabel("$\phi(t) /\  \psi(\\tau)$")
plt.legend(["$\psi(\\tau)$", "$\phi(t)$"])
plt.title("Numerical/analytical inflation")
plt.show()


plt.plot(tau, h_vals)
plt.xlabel("Time $\\tau$")
plt.ylabel("h")
plt.legend(["$ln[a(\\tau)/a_i]$"])
plt.title("h")
print(h_vals[-1])
plt.show()

plt.plot(tau, p)
plt.xlabel("Time $\\tau$")
plt.ylabel("p")
plt.legend(["$p_{\phi}$"])
plt.title("Pressure")
plt.show()
