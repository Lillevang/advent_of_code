import sys
import time
from typing import Iterable, List, Tuple, Literal

Direction = Literal["L", "R"]
Move = Tuple[Direction, int]

DIAL_SIZE = 100
START_POS = 50

# ANSI colors
GREEN = "\x1b[32m"
BRIGHT_GREEN = "\x1b[92m"
BOLD = "\x1b[1m"
RESET = "\x1b[0m"


# ------------- Parsing -------------

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


# ------------- Core logic -------------

def move(pos: int, direction: Direction, distance: int) -> int:
    if direction == "R":
        return (pos + distance) % DIAL_SIZE
    else:
        return (pos - distance) % DIAL_SIZE


def compute_password(moves: Iterable[Move]) -> int:
    """Part 1: count how many moves end at position 0."""
    pos = START_POS
    hits = 0
    for direction, distance in moves:
        pos = move(pos, direction, distance)
        if pos == 0:
            hits += 1
    return hits


def count_zero_hits_during_rotation(pos: int, direction: Direction, distance: int) -> int:
    """Part 2 helper: math shortcut – how many times this move passes 0."""
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
    """Part 2: using the math shortcut for all moves."""
    pos = START_POS
    hits_zero = 0

    for direction, distance in moves:
        hits_zero += count_zero_hits_during_rotation(pos, direction, distance)
        pos = move(pos, direction, distance)

    return hits_zero


# ------------- Visualization helpers -------------

def render_dial(pos: int) -> str:
    """Render dial as one line.

    - '.' everywhere
    - '0' at position 0
    - 'X' at current position
    - bright green 'X' if current pos == 0
    """
    chars = []
    for i in range(DIAL_SIZE):
        if i == pos == 0:
            chars.append(f"{BRIGHT_GREEN}{BOLD}X{RESET}")
        elif i == pos:
            chars.append("X")
        elif i == 0:
            chars.append("0")
        else:
            chars.append(".")
    return "".join(chars)


# ------------- Part 1 animation (per move) -------------

def animate_part1(moves: List[Move], delay: float = 0.10) -> None:
    pos = START_POS
    hits_zero = 0
    total_moves = len(moves)

    print("Part 1 dial animation (per move)\n")

    # Initial render (6 content lines + 1 spacer)
    dial_line = render_dial(pos)
    pos_line = f"pos={pos}"
    move_line = f"move=0/{total_moves}"
    dir_line = "direction=--"
    hits_line = f"hits_zero={hits_zero}"
    hit_this_line = " "
    spacer_line = ""

    print(dial_line)
    print(pos_line)
    print(move_line)
    print(dir_line)
    print(hits_line)
    print(hit_this_line)
    print(spacer_line, end="", flush=True)  # cursor on spacer

    for idx, (direction, distance) in enumerate(moves, start=1):
        pos = move(pos, direction, distance)
        hit_this = (pos == 0)
        if hit_this:
            hits_zero += 1

        dial_line = render_dial(pos)
        pos_line = f"pos={pos}"
        move_line = f"move={idx}/{total_moves}"
        dir_line = f"direction={direction}{distance}"
        hits_line = f"hits_zero={hits_zero}"

        if hit_this:
            hit_this_line = (
                f"{BOLD}{BRIGHT_GREEN}*** HIT 0! hits_zero={hits_zero} ***{RESET}"
            )
        else:
            hit_this_line = " "

        # Move cursor up 7 lines (dial + 5 info + spacer) and clear down
        sys.stdout.write("\x1b[7F")
        sys.stdout.write("\x1b[0J")

        print(dial_line)
        print(pos_line)
        print(move_line)
        print(dir_line)
        print(hits_line)
        print(hit_this_line)
        print(spacer_line, end="", flush=True)

        time.sleep(delay)

    print("\n\nDone P1. Final hits_zero =", hits_zero)


# ------------- Part 2 animation (per click) -------------

def animate_part2(moves: List[Move], delay: float = 0.01, max_clicks: int | None = 5000) -> None:
    """Animate Part 2 logic: every single click.

    Note: if input has huge distances, max_clicks keeps it from running forever.
    """
    pos = START_POS
    hits_zero = 0
    total_moves = len(moves)
    total_clicks = 0

    print("Part 2 dial animation (per click)\n")

    # Initial render (7 content lines + 1 spacer)
    dial_line = render_dial(pos)
    pos_line = f"pos={pos}"
    move_line = f"move=0/{total_moves}"
    dir_line = "direction=--"
    move_click_line = "click_in_move=0/0"
    hits_line = f"hits_zero={hits_zero}"
    hit_this_line = " "
    spacer_line = ""

    print(dial_line)
    print(pos_line)
    print(move_line)
    print(dir_line)
    print(move_click_line)
    print(hits_line)
    print(hit_this_line)
    print(spacer_line, end="", flush=True)

    for move_idx, (direction, distance) in enumerate(moves, start=1):
        step = 1 if direction == "R" else -1

        for click_in_move in range(1, distance + 1):
            if max_clicks is not None and total_clicks >= max_clicks:
                print("\n\nReached max_clicks, stopping animation.")
                print("Current hits_zero (simulated):", hits_zero)
                return

            pos = (pos + step) % DIAL_SIZE
            total_clicks += 1

            hit_this = (pos == 0)
            if hit_this:
                hits_zero += 1

            dial_line = render_dial(pos)
            pos_line = f"pos={pos}"
            move_line = f"move={move_idx}/{total_moves}"
            dir_line = f"direction={direction}{distance}"
            move_click_line = f"click_in_move={click_in_move}/{distance}   total_clicks={total_clicks}"
            hits_line = f"hits_zero={hits_zero}"

            if hit_this:
                hit_this_line = (
                    f"{BOLD}{BRIGHT_GREEN}*** HIT 0! hits_zero={hits_zero} ***{RESET}"
                )
            else:
                hit_this_line = " "

            # Move cursor up 8 lines (dial + 6 info lines + spacer) and clear
            sys.stdout.write("\x1b[8F")
            sys.stdout.write("\x1b[0J")

            print(dial_line)
            print(pos_line)
            print(move_line)
            print(dir_line)
            print(move_click_line)
            print(hits_line)
            print(hit_this_line)
            print(spacer_line, end="", flush=True)

            time.sleep(delay)

    print("\n\nDone P2 animation. Final hits_zero (simulated) =", hits_zero)


# ------------- Main -------------

if __name__ == "__main__":
    with open("input", "r", encoding="utf-8") as f:
        raw = f.read()

    moves = parse_moves(raw)

    part1 = compute_password(moves)
    part2 = compute_password_method_click(moves)

    print("Part 1:", part1)
    print("Part 2:", part2)

    input("\nPress Enter to run P1 animation...")
    # animate_part1(moves, delay=0.05)

    input("\nPress Enter to run P2 animation (per click)...")
    animate_part2(moves, delay=0.01, max_clicks=5000)
