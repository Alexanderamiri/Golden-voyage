import numpy as np
import matplotlib.pyplot as plt

n = 8192
sampling = 10e3
f1 = 1000
f2 = 1600
c1 = 1
c2 = 1.7
T = n / sampling
frekv = np.linspace(0, sampling / 2, int(n / 2))
t = np.linspace(0, T, n)
dt = T / n
t1 = 0.15
t2 = 0.5
sigma1 = 0.01
sigma2 = 0.1


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


def func(x):
    return c1 * np.sin(2 * np.pi * f1 * x) + c2 * np.sin(2 * np.pi * f2 * x)


def func2(x):
    return c1 * np.sin(2 * np.pi * f1 * x) * np.exp(
        -(((x - t1) / (sigma1)) ** 2)
    ) + c2 * np.sin(2 * np.pi * f2 * x) * np.exp(-(((x - t2) / (sigma2)) ** 2))


pl2 = t[100:500]
plt.subplot(2, 1, 1)
plt.ylabel("Frekvens")
plt.xlabel("Time [s]")
plt.plot(t, func(t))
plt.subplot(2, 1, 2)
plt.ylabel("Frekvens")
plt.xlabel("Time [s]")
plt.plot(pl2, func(pl2))
plt.show()

k = np.fft.fft(func(t), n) / n
plt.ylabel("Amplitude")
plt.xlabel("Frequency [Hz]")
plt.plot(frekv, 2 * abs(k[0 : int(n / 2)]))
plt.show()

omega = 2 * np.pi * np.logspace(np.log10(800), np.log10(2000), 1000)
k24 = wavelet_diagram(t, func(t), omega, 24)
k100 = wavelet_diagram(t, func(t), omega, 100)
plt.subplot(2, 1, 1)
plt.pcolormesh(t, omega / (2 * np.pi), abs(k24), cmap="jet")
plt.colorbar()
plt.subplot(2, 1, 2)
plt.pcolormesh(t, omega / (2 * np.pi), abs(k100), cmap="jet")
plt.colorbar()
plt.show()

kk = np.fft.fft(func2(t), n) / n
omega = 2 * np.pi * np.logspace(np.log10(800), np.log10(2000), 1000)
k24 = wavelet_diagram(t, func2(t), omega, 24)
k100 = wavelet_diagram(t, func2(t), omega, 100)

plt.subplot(4, 1, 1)
plt.ylabel("Frekvens")
plt.xlabel("Time [s]")
plt.plot(t, func2(t))
plt.subplot(4, 1, 2)
plt.ylabel("Amplitude")
plt.xlabel("Frequency [Hz]")
plt.plot(frekv, 2 * abs(kk[0 : int(n / 2)]))
plt.subplot(4, 1, 3)
plt.pcolormesh(t, omega / (2 * np.pi), abs(k24), cmap="jet")
plt.colorbar()
plt.subplot(4, 1, 4)
plt.pcolormesh(t, omega / (2 * np.pi), abs(k100), cmap="jet")
plt.colorbar()
plt.show()
