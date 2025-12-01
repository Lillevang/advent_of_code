
with open('input', 'r') as f:
    data = f.read()


def compute_password(raw: str) -> int:

    pos = 50
    hist_zero = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        if direction == 'L':
            pos = (pos - distance) % 100
        elif direction == 'R':
            pos = (pos + distance) % 100
        else:
            raise ValueError(f"Invalid direction: {direction}")

        if pos == 0:
            hist_zero += 1
    return hist_zero


# TODO: Refactor to avoid dups
def count_zero_hits_during_rotation(pos: int, direction: str, distance: int) -> int:
    if distance <= 0:
        return 0

    if direction == 'R':
        first_step = (100 - pos) % 100
    elif direction == 'L':
        first_step = pos % 100
    else:
        raise ValueError(f"Invalid direction: {direction}")

    # If first_step == 0, it means we'd hit 0 after a full turn of 100 clicks
    if first_step == 0:
        first_step = 100

    if distance < first_step:
        return 0

    return 1 + (distance - first_step) // 100


def compute_password_method_click(raw: str) -> int:
    pos = 50
    hits_zero = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        hits_zero += count_zero_hits_during_rotation(pos, direction, distance)

        if direction == 'R':
            pos = (pos + distance) % 100
        else:  # 'L'
            pos = (pos - distance) % 100

    return hits_zero


print(f"Part 1: {compute_password(data)}")
print(f"Part 2: {compute_password_method_click(data)}")
