import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the Bezier curve function
def bezier_curve(t, p0, p1, p2, p3):
    return (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t) * t**2 * p2 + t**3 * p3

# Define the points for the first Bezier curve
p0_1 = np.array([24.93, 120.27])
p1_1 = np.array([68.53, 64.8])
p2_1 = np.array([110.4, 119.73])
p3_1 = np.array([110.8, 119.73])

# Define the points for the second Bezier curve
p0_2 = np.array([110.8, 119.73])
p1_2 = np.array([111.07, 120.13])
p2_2 = np.array([71.73, 143.87])
p3_2 = np.array([25.2, 120.93])

# Generate the points for the curves
t = np.linspace(0, 1, 100)
curve1 = np.array([bezier_curve(ti, p0_1, p1_1, p2_1, p3_1) for ti in t])
curve2 = np.array([bezier_curve(ti, p0_2, p1_2, p2_2, p3_2) for ti in t])

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 150)
ax.set_ylim(0, 150)
line1, = ax.plot([], [], label='Curve 1')
line2, = ax.plot([], [], label='Curve 2')
control_points = ax.scatter([24.93, 68.53, 110.4, 110.8, 111.07, 71.73, 25.2], 
                            [120.27, 64.8, 119.73, 119.73, 120.13, 143.87, 120.93], 
                            color='red')  # Control points
ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Bezier Curves')
ax.grid(True)

# Initialization function
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

# Animation function
def animate(i):
    alpha = i / 100
    linear1 = (1 - alpha) * np.linspace(p0_1, p3_1, 100) + alpha * curve1
    linear2 = (1 - alpha) * np.linspace(p0_2, p3_2, 100) + alpha * curve2
    line1.set_data(linear1[:, 0], linear1[:, 1])
    line2.set_data(linear2[:, 0], linear2[:, 1])
    return line1, line2

# Create the animation
ani = FuncAnimation(fig, animate, init_func=init, frames=101, interval=2, blit=True)

plt.show()