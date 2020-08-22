from matplotlib.pyplot import plot, show
from numpy import zeros, select

b = 0.1
m = 0.1
g = 9.81
k = 100
u = 0.1
mu_d = 0.3
mu_s = 0.6
dt = 0.001
Tim = 2
n = int(Tim/dt)
v = zeros(n+1)
xt = zeros(n+1)
t = zeros(n+1)
xb = zeros(n+1)
spring = zeros(n+1)
xb[0] = b
v[0] = 0


def fstatic(t, v, x, xbb):
    if v == 0:
        if k*(xbb-x-b) <= mu_s*m*g:
            return k*(xbb-x-b)
        else:
            return 0
    else:
        return 0


fdyn = lambda v: select([v < 0, v == 0, v > 0], [m*g*mu_d, 0, -m*g*mu_d])

for i in range(n):
    a = k / m * (xb[i]-xt[i]-b) + fdyn(v[i])/m + fstatic(t[i], v[i], xt[i], xb[i])/m
    spring[i+1] = k * (xb[i]-xt[i]-b)
    v[i+1] = v[i]+a*dt
    xt[i+1] = xt[i] + v[i+1]*dt
    xb[i+1] = xb[i] + u*dt
    t[i+1] = t[i] + dt

plot(t, spring)
show()
