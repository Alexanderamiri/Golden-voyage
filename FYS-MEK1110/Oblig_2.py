from numpy import sin, cos, zeros, sqrt, array, pi
from matplotlib.pyplot import plot, legend, xlabel, ylabel, title, show

m = 0.1
theta = 30
k = 200
T = 10
dt = 0.001
n = int(T/dt)
L0 = 1
g = 9.81
x = sin(pi/6)
y = cos(pi/6)

r = zeros((n+1, 2))
v = zeros((n+1, 2))
t = zeros(n+1)
r[0] = x, y

for i in range(n):
    a = -g*array([0, 1])-k*(sqrt(r[i, 0]**2+r[i, 1]**2)-L0)*r[i]/(sqrt(r[i, 0]**2+r[i, 1]**2))
    v[i+1, :] = v[i, :] + a*dt
    r[i+1, :] = r[i, :] + v[i+1]*dt
    t[i+1] = t[i]+dt
plot(r[:, 0], r[:, 1], c='green')
xlabel('X')
ylabel('Y')
title('Pendel')
legend(['Pendel ball', 'Velocity'])
show()

