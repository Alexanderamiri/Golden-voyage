from numpy import *
from matplotlib.pyplot import *


def exact(x):
    return (exp(2*x)-1)/(exp(2*x)+1)


def f(x):
    return 1-x**2


def Forwardeuler(f, x0, T, n):
    x = zeros(n+1)
    t = linspace(0,T, n+1)
    dt = T/n
    for i in range(n):
        x[i+1] = x[i]+dt*f(x[i])
    return x, t


def midtpointmethod(f, x0, T, n):
    x = zeros(n+1)
    t = linspace(0,T, n+1)
    dt = T/n
    for i in range(n):
        k = x[i]+1/2*dt*f(x[i])
        x[i + 1] = x[i] + dt*f(k)
    return x, t


tx = linspace(0, 2, 1000)

x1, t1 = Forwardeuler(f, 0, 2, 5)
x2, t2 = midtpointmethod(f, 0, 2, 5)
plot(t1, x1)
plot(t2, x2)
plot(tx, exact(tx))
xlabel('t')
ylabel('x(t)')
legend(['Forward euler', 'Midtpoint', 'Exact'])
savefig('Oppgave2finish.png')
show()
