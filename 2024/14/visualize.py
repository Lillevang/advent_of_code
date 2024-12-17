import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

with open('input', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

T = 100
WIDTH = 101
HEIGHT = 103
START_ITERATION = 7500  # Start animation from iteration 7500
TARGET_ITERATION = 7571  # Stop and linger at this iteration
LINGER_FRAMES = 50  # Number of extra frames to linger on the final state


def solve(lines):
    positions = []
    velocities = []

    # Extract initial data
    for line in lines:
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        positions.append((px, py))  # Store initial positions
        velocities.append((vx, vy))  # Store velocities

    # Move positions to their state at iteration 7500
    for i in range(len(positions)):
        px, py = positions[i]
        vx, vy = velocities[i]
        positions[i] = ((px + vx * START_ITERATION) % WIDTH, (py + vy * START_ITERATION) % HEIGHT)

    def update(frame):
        """Update function for animation."""
        nonlocal positions

        # Compute the current iteration
        if frame < TARGET_ITERATION - START_ITERATION:
            # Dynamically update positions
            for i in range(len(positions)):
                px, py = positions[i]
                vx, vy = velocities[i]
                positions[i] = ((px + vx) % WIDTH, (py + vy) % HEIGHT)

            # Update scatter plot for dynamic frames
            x, y = zip(*positions)
            scatter.set_offsets(list(zip(x, y)))
            title.set_text(f"Iteration: {START_ITERATION + frame + 1}")
        else:
            # Linger on the final frame
            x, y = zip(*positions)
            scatter.set_offsets(list(zip(x, y)))
            title.set_text(f"Iteration: {TARGET_ITERATION + 1} (Final State)")

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.invert_yaxis()  # Flip the y-axis to make the tree upright
    ax.set_aspect('equal')
    scatter = ax.scatter([], [], s=10, c='blue')  # Initial empty scatter
    title = ax.set_title(f"Iteration: {START_ITERATION}")

    # Create animation for frames from 7500 to 7572 plus lingering frames
    dynamic_frames = TARGET_ITERATION - START_ITERATION
    total_frames = dynamic_frames + LINGER_FRAMES
    ani = FuncAnimation(fig, update, frames=range(total_frames), interval=100)

    # Save the animation as a GIF
    ani.save("christmas_tree.gif", writer="pillow", fps=10)
    print("GIF saved as 'christmas_tree.gif'")

solve(lines)
