import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sc

k1 = 4
k2 = 2
x = [0, 0.8, 0, -0.8]

samplingrate = 10
dt = 1 / (2 * samplingrate)
N = 10000
frekv = np.linspace(0, samplingrate / 2, int(N / 2))


def dobbel_oscillator(t, u):
    return u[1], -k1 * u[0] + k2 * (u[2] - u[0]), u[3], -k2 * (u[2] - u[0])


def morlet(omega1, omega2, k):
    return 2 * (
        np.exp(-((k * (omega1 - omega2) / omega2) ** 2))
        - np.exp(-(k ** 2)) * np.exp(-((k * omega1 / omega2) ** 2))
    )


def wavelet_transform(t, signal, omega, k):
    signal = np.fft.fft(signal)
    omeg = 2 * np.pi * np.fft.fftfreq(len(signal), dt)
    return np.fft.ifft(morlet(omeg, omega, k) * signal)


def wavelet_diagram(t, signal, omega, k):
    signals = []
    for i in range(len(omega)):
        signals.append(wavelet_transform(t, signal, omega[i], k))
    return np.array(signals)


t = np.linspace(0, 1000, N)
z = sc.solve_ivp(dobbel_oscillator, [0, 1000], x, method="RK45", t_eval=t)
plt.plot(z.t[0:1000], z.y[0, 0:1000])
plt.plot(z.t[0:1000], z.y[2, 0:1000])
plt.xlabel("Tid [s]")
plt.ylabel("Frekvens")
plt.show()

k = np.fft.fft(z.y[0]) / N
plt.plot(frekv, 2 * abs(k[0 : int(N / 2)]))
plt.ylabel("Amplitude")
plt.xlabel("Frekvens")
plt.show()

omega = np.linspace(0, 5, 100)
k24 = wavelet_diagram(z.t, z.y[0], omega, 24)
kk24 = wavelet_diagram(z.t, z.y[2], omega, 24)
k100 = wavelet_diagram(z.t, z.y[0], omega, 100)
kk100 = wavelet_diagram(z.t, z.y[2], omega, 100)
plt.subplot(4, 1, 1)
plt.title("x_1 with k=24")
plt.pcolormesh(t, omega / (2 * np.pi), np.sqrt(abs(k24)), cmap="jet")
plt.colorbar()
plt.subplot(4, 1, 2)
plt.title("x_2 with k=24")
plt.pcolormesh(t, omega / (2 * np.pi), np.sqrt(abs(kk24)), cmap="jet")
plt.colorbar()
plt.subplot(4, 1, 3)
plt.title("x_1 with k=100")
plt.pcolormesh(t, omega / (2 * np.pi), np.sqrt(abs(k100)), cmap="jet")
plt.colorbar()
plt.subplot(4, 1, 4)
plt.title("x_2 with k=100")
plt.pcolormesh(t, omega / (2 * np.pi), np.sqrt(abs(kk100)), cmap="jet")
plt.colorbar()
plt.show()
