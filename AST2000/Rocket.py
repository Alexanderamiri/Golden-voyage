import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


class Rocket:
    """A class to simulate a rocket energy output using statistical physics
    and thermodynamics"""

    def __init__(self):
        self.H2gPrMol = 2.01588  # Hydrogen gass weight [g/mol]
        self.N_a = 6.02214179e23  # Avogadros number
        self.mass_sat = 1100  # Satellite/Rocket mass [kg]
        self.k = 1.380648e-23  # Boltzmann's constant [J/K]
        self.mass1Particle = self.H2gPrMol / self.N_a * 1e-3  # [kg]

    def simulate_box(self, n, Nt, dt, box_dim, T):
        sigma = np.sqrt(self.k * T / self.mass1Particle)  # Standard deviation
        mean = 0  # Mean
        L = 10 ** -6  # Size of box
        np.random.seed(8)

        pos = np.random.uniform(0, L, [n, 3, Nt])  # ... uniform dist.
        vel = np.random.normal(mean, sigma, (n, 3))  # ... Gauss dist.
        x_momentum = 0.0  # Momentum
        no_escapes = 0  # Counter
        xminus = np.zeros(n, dtype=bool)

        for i in range(Nt - 1):  # Time loop
            pos[:, :, i + 1] = pos[:, :, i] + vel[:, :] * dt
            # Move ALL particles one step
            vel[pos[:, :, i + 1] > box_dim] *= -1  # turning
            # all particles that are out of the box
            vel[pos[:, :, i + 1] < 0] *= -1

            xminus[:] = pos[:, 0, i + 1] >= box_dim
            yhole = np.logical_and(
                pos[:, 1, i + 1] >= 1 / 4 * box_dim,
                pos[:, 1, i + 1] <= 3 / 4 * box_dim,
            )
            zhole = np.logical_and(
                pos[:, 2, i + 1] >= 1 / 4 * box_dim,
                pos[:, 2, i + 1] <= 3 / 4 * box_dim,
            )
            hole_yx = np.logical_and(yhole, zhole)  # Putting together the y
            # and z interval of the hole
            hole_xyz = np.logical_and(hole_yx, xminus)  # evaluating the yz

            x_momentum += sum(vel[hole_xyz, 0]) * self.mass1Particle * 2
            no_escapes += sum(hole_xyz)
        self.force = x_momentum / (dt * Nt)
        self.massperssecond = no_escapes * self.mass1Particle / (dt * Nt)
        self.deltav = x_momentum / (1000)
        self.accel = self.deltav / (Nt * dt)
        print("momentum= ", x_momentum)
        print("no_escapes= ", no_escapes)
        print("force= ", self.force)
        print("mass/s= ", self.massperssecond)
        print("deltav= ", self.deltav)
        print("accel= ", self.accel)
        return x_momentum, pos

    def launch_sim(self, no_boxes, v_end, A, no_particles_sec):
        multiplier = 120
        force = A * no_boxes * multiplier  # (dp/dt) for whole engine
        B = (
            no_particles_sec * no_boxes * multiplier
        )  # (insert value)  # dm/dt for the box described in first method
        v = 0  # initial velocity relative to surface of planet
        time = 0.0  # initialize time variable
        # gravity = 11.665653831124791
        T = 40.0 * 60  # Total time, 20 minutes
        Nt = 100000  # Number of time steps
        homemassskg = 8.990640113718568e24
        homeradius = 7171.9370402 * 1e3
        dt = float(T) / Nt  # Time step
        g = 6.67408e-11
        initial_fuel_mass = 101000  # Calculate/set fuel mass
        M = self.mass_sat + initial_fuel_mass  # Total mass
        posi = 1
        for i in range(Nt):
            gravity = 0
            v += (force - gravity) * dt / M
            M -= B * dt
            posi += v * dt
            time += dt

            if M < self.mass_sat:
                print("You've run out of fuel")
                continue
            elif v < 0:
                "nothing"
            elif v >= v_end:
                fuel_needed = (self.mass_sat + initial_fuel_mass) - M
                return fuel_needed, time, posi
        return 0, 0, 0  # returns 0 because the boost was not successful.

    def plot(self, n, Nt, dt, box_dim, T):
        def update_lines(num, dataLines, lines):
            for line, data in zip(lines, dataLines):
                line.set_data(data[0:2, num - 1 : num])
                line.set_3d_properties(data[2, num - 1 : num])
            return lines

        # Attach 3D axis to the figure
        fig = plt.figure()
        ax = p3.Axes3D(fig)
        m = 1000
        # Run the actual simulation
        x_momentum, datax = self.simulate_box(n, Nt, dt, box_dim, T)
        lines = []
        data = []
        for i in range(n):
            data.append(
                [datax[i]]
            )  # wrap data inside another layer of [], needed for animation!
            lines.append(
                [
                    ax.plot(
                        data[i][0][0, 0:1],
                        data[i][0][1, 0:1],
                        data[i][0][2, 0:1],
                        "o",
                    )[0]
                ]
            )
        # Set the axes properties
        ax.set_xlim3d([0.0, box_dim])
        ax.set_xlabel("X")

        ax.set_ylim3d([0.0, box_dim])
        # x.set_ylabel('Y')

        ax.set_zlim3d([0.0, box_dim])
        ax.set_zlabel("Z")
        # plt.axis('off')
        ax.set_title("Particle Animation")

        # Creating the Animation object
        ani = [i for i in range(n)]  # "Initialize" a list of length n

        for i in range(n):
            # This is the method that needs the elements of data and
            # lines to be wrapped in two layers of []
            ani[i] = animation.FuncAnimation(
                fig,
                update_lines,
                m,
                fargs=(data[i], lines[i]),
                interval=50,
                blit=False,
            )
        plt.show()


if __name__ == "__main__":
    instance = Rocket()
    instance.simulate_box(box_dim=1e-6, n=100000, Nt=1000, dt=1e-12, T=20000)
    solarmass = 1.98855e30
    grav = 6.67408e-11
    homemass = 1.0633682797535578e-05  # solarmasses
    homemasskg = homemass * solarmass
    homeradius = 9251.914528048517  # km
    escapevelocity = np.sqrt(2 * grav * homemasskg / (homeradius * 1e3))
    escapetime = 20 * 60
    escapeaccel = escapevelocity / escapetime
    no_boxess = escapeaccel / (3.37403098212e-12)
    print(homemasskg * grav / ((homeradius * 1e3) ** 2))
    print("escapevelocity= ", escapevelocity)
    print("no_boxes= ", no_boxess)
    fuel, time, posi = instance.launch_sim(
        no_boxess, 12935.6356481, 6.71080500101e-09, 2.96305959213e-13
    )
    # 20k
    fuel, time, posi = instance.launch_sim(
        no_boxess, 12935.6356481, 3.37403098212e-09, 2.10571148641e-13
    )
    # 10k hydrogen
    print("fuel, time, position =", fuel, time, posi)
"""
momentum=  -6.67998553634481e-18
no_escapes=  88038
force=  -6.67998553634481e-09
mass/s=  2.9470253213682637e-13
deltav=  -6.67998553634481e-21
accel=  -6.67998553634481e-12
16.487256733380544
escapevelocity=  17466.464444714
no_boxes=  4313945874947.51
fuel, time, position = 56558.99024745462 518.8560000000188 2909374.9264573716


"""
