from numpy import zeros,exp
from matplotlib.pyplot import plot, subplot, legend, show


def f(u, t):
    return (400+f_c*exp(-(t/t_c)**2)-f_v*u-(1/2*rho*C_d*A*(1-0.25*exp(-(t/t_c)**2))*(u-w)**2))/80


rho = 1.293
m = 80
C_d = 1.2
w = -1
A = 0.45
F = 400
t_c = 0.67
f_v = 25.8
f_c = 488
n = 100000
T = 15
dt = T/n
x = zeros(n+1)
v = zeros(n+1)
a = zeros(n+1)
t = zeros(n+1)

i = 0
while x[i] <= 100:
    a[i] = (400-(1/2*rho*C_d*A*(v[i]-w)**2))/80
    v[i+1] = v[i]+f(v[i], i)*dt
    x[i+1] = x[i]+v[i+1]*dt
    t[i+1] = t[i] + dt
    i += 1

subplot(3, 1, 1)
plot(t[:i], x[:i], 'g')
legend(['Position'], loc='best')
subplot(3, 1, 2)
plot(t[:i], v[:i], 'r')
legend(['Velocity'], loc='best')
subplot(3, 1, 3)
plot(t[:i], a[:i])
legend(['Acceleration'], loc='best')


print(t[i])
print(x[i])

show()

'''
10.01682
100.000096834

'''