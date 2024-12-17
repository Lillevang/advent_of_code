import re

with open('input', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

T = 100
WIDTH = 101
HEIGHT = 103

q1 = q2 = q3 = q4 = 0
positions = []
velocities = []

# First pass: extract initial data
for line in lines:
    px, py, vx, vy = map(int, re.findall(r'-?\d+', line))

    # Handle Part 1: Compute final positions after T time units
    x_final = (px + vx * T) % WIDTH
    y_final = (py + vy * T) % HEIGHT
    positions.append((px, py))   # Store initial positions
    velocities.append((vx, vy))  # Store velocities

    # Determine quadrant
    x_mid = WIDTH // 2
    y_mid = HEIGHT // 2
    if x_final < x_mid and y_final < y_mid:
        q1 += 1
    elif x_final < x_mid and y_final >= y_mid:
        q2 += 1
    elif x_final >= x_mid and y_final < y_mid:
        q3 += 1
    elif x_final >= x_mid and y_final >= y_mid:
        q4 += 1

# Part 1 result
print(q1 * q2 * q3 * q4)

# Part 2: Find the time when all positions are distinct
t = 0
while True:
    distinct_positions = set(positions)
    if len(distinct_positions) == len(positions):
        break
    for i in range(len(positions)):
        px, py = positions[i]
        vx, vy = velocities[i]
        positions[i] = ((px + vx) % WIDTH, (py + vy) % HEIGHT)
    t += 1
    if t == 8000:  # Timeout limit
        break

# Part 2 result
print(t)
