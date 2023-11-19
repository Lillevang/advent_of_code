with open('./input', 'r') as file:
    lines = file.readlines()

rope_positions = [0] * 10
seen_positions = [set([x]) for x in rope_positions]
directions = {'L': 1, 'R': -1, 'D': 1j, 'U': -1j}

def get_sign(x):
    return complex((x.real > 0) - (x.real < 0), (x.imag > 0) - (x.imag < 0))

for line in lines:
    for _ in range(int(line[2:])):
        rope_positions[0] += directions[line[0]]

        for i, position in enumerate(rope_positions[1:], start=1):
            distance = rope_positions[i - 1] - position
            if abs(distance) >= 2:
                rope_positions[i] += get_sign(distance)
                seen_positions[i].add(rope_positions[i])

# Part One
print(len(seen_positions[1]))

# Part Two
print(len(seen_positions[9]))
