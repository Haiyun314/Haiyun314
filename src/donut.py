import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# game of life (rules)
# Any live cell with fewer than two live neighbors dies (underpopulation).
# Any live cell with two or three live neighbors lives on to the next generation (survival).
# Any live cell with more than three live neighbors dies (overpopulation).
# Any dead cell with exactly three live neighbors becomes a live cell (reproduction).

root_path = os.path.join(os.path.abspath(__file__), os.pardir, os.pardir)

grid = 100
domain = np.round(np.random.randint(0, 7, size= (grid, grid))/10)



# Create a meshgrid for the 2D plane (u, v)
u = np.linspace(0, 1, grid)
v = np.linspace(0, 1, grid)
u, v = np.meshgrid(u, v)

# create donut
R = 1  #  radius 
r = 0.3  
x = (R + r * np.cos(2 * np.pi * v)) * np.cos(2 * np.pi * u)
y = (R + r * np.cos(2 * np.pi * v)) * np.sin(2 * np.pi * u)
z = r * np.sin(2 * np.pi * v)


fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111, projection='3d')


def update():
    global domain
    reset_domain = domain.copy()
    for i in range(grid):
        for j in range(grid):
            neibers = np.sum(domain[i-1:i+2, j-1:j+2]) - domain[i, j]
            if neibers >= 4 or neibers < 2:
                reset_domain[i, j] = 0
            elif neibers == 3:
                reset_domain[i, j] = 1
    
    domain = reset_domain
    return domain.astype(np.int0)


def evol(frame):
    ax.cla()
    ax.plot_surface(x, y, z, cmap='hot_r')
    #project the 2d game of life to 3d donut
    cur = update()
    mask = cur == 1
    x_p = x * cur
    x_p = x_p[mask]
    y_p = y * cur
    y_p = y_p[mask]
    z_p = z * cur
    z_p = z_p[mask]

    ax.scatter(x_p, y_p, z_p, color = 'y', s=5)
    # Labels and title
    ax.set_axis_off()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("Play game of life on Donut")

ani = FuncAnimation(fig, evol, frames= 20)
image_path = os.path.abspath(os.path.join(root_path, 'results', 'torus_animation.gif'))
ani.save(image_path, writer='pillow')


