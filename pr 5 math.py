import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

num_particles = 20
center = np.array([0.0, 0.0])
duration = 10 
max_speed = 0.2 

angles = np.random.uniform(0, 2 * np.pi, num_particles)
speeds = np.random.uniform(0.01, max_speed, num_particles)
velocities = np.array([np.cos(angles) * speeds, np.sin(angles) * speeds]).T

positions = np.tile(center, (num_particles, 1))

fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
particles, = ax.plot([], [], 'bo', markersize=5)

def init():
    particles.set_data([], [])
    return particles,

def update(frame):
    global positions
    positions += velocities 
    particles.set_data(positions[:, 0], positions[:, 1])
    return particles,

ani = FuncAnimation(fig, update, frames=duration, init_func=init, blit=True)

plt.show()
