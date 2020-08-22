from numpy import linspace, zeros
from matplotlib.pyplot import plot, legend, xlabel, ylabel, title, show

t = linspace(0, 6, 1000)
dt = t[1]-t[0]
v = zeros(len(t))
x = zeros(len(t))
x[0] = -5
v0 = linspace(8, 10, 10000)
m = 23
U0 = 150
alpha = 39.48
x0 = 2


def f(x):
    if abs(x) < x0:
        return -(U0*x)/(abs(x)*x0)
    else:
        return 0


def f0(x, v):
    if abs(x) < x0:
        return -alpha*v
    else:
        return 0


bl = 0
for k in v0:
    v[0] = k
    for i in range(len(t)-1):
        a = f(x[i])/m + f0(x[i], v[i])/m
        v[i+1] = v[i] + a*dt
        x[i+1] = x[i] + v[i+1]*dt
    plot(t, x, label='v0 = {}'.format(k))
    for j in v:
        if j < 0:
            bl = k
            break
title('Position of particle')
print('Maxiumum velocity and still trapped = ' ,bl)
legend(['V0=8', 'V0 = 10'])
xlabel('t')
ylabel('x')
show()

'''
maximum velocity and still trapped =  8.80068006801

Process finished with exit code 0
'''