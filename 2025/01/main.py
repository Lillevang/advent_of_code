from typing import Iterable, List, Tuple, Literal

Direction = Literal["L", "R"]
Move = Tuple[Direction, int]

DIAL_SIZE = 100
START_POS = 50


def parse_moves(raw: str) -> List[Move]:
    moves: List[Move] = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        if direction not in ("L", "R"):
            raise ValueError(f"Invalid direction: {direction}")

        distance = int(line[1:])
        moves.append((direction, distance))

    return moves


def move(pos: int, direction: Direction, distance: int) -> int:
    if direction == "R":
        return (pos + distance) % DIAL_SIZE
    else:  # "L"
        return (pos - distance) % DIAL_SIZE


def compute_password(moves: Iterable[Move]) -> int:
    pos = START_POS
    hits_zero = 0

    for direction, distance in moves:
        pos = move(pos, direction, distance)
        if pos == 0:
            hits_zero += 1

    return hits_zero


def count_zero_hits_during_rotation(pos: int, direction: Direction, distance: int) -> int:
    if distance <= 0:
        return 0

    if direction == "R":
        first_step = (DIAL_SIZE - pos) % DIAL_SIZE
    else:  # "L"
        first_step = pos % DIAL_SIZE

    # If first_step == 0, it means we'd hit 0 after a full turn
    if first_step == 0:
        first_step = DIAL_SIZE

    if distance < first_step:
        return 0

    return 1 + (distance - first_step) // DIAL_SIZE


def compute_password_method_click(moves: Iterable[Move]) -> int:
    pos = START_POS
    hits_zero = 0

    for direction, distance in moves:
        hits_zero += count_zero_hits_during_rotation(pos, direction, distance)
        pos = move(pos, direction, distance)

    return hits_zero


if __name__ == "__main__":
    with open("input", "r", encoding="utf-8") as f:
        raw = f.read()

    moves = parse_moves(raw)

    print(f"Part 1: {compute_password(moves)}")
    print(f"Part 2: {compute_password_method_click(moves)}")
