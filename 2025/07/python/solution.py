from typing import List, Tuple, Dict
from collections import defaultdict
import sys


def read_input() -> List[List[str]]:
    with open('./input', 'r') as file:
        lines = [line.rstrip("\n") for line in file]
    lines = [line for line in lines if line]
    return [list(line) for line in lines]


def find_start(grid: List[List[str]]) -> Tuple[int, int]:
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                return r, c
    raise ValueError("No S found in grid")


def simulate(grid: List[List[str]]) -> Tuple[int, int]:
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    start_row, start_col = find_start(grid)

    # Initial beams: one beam in the start column
    beams: Dict[int, int] = {start_col: 1}
    splits = 0

    # Process rows below the start row
    for r in range(start_row + 1, height):
        row = grid[r]

        if "^" not in row:
            continue

        next_beams: Dict[int, int] = defaultdict(int)

        for x, count in beams.items():
            # If a beam has somehow gone out of bounds, ignore it
            if x < 0 or x >= width:
                continue

            if row[x] == "^":
                splits += 1
                # Spawn beams to the left and right
                if x - 1 >= 0:
                    next_beams[x - 1] += count
                if x + 1 < width:
                    next_beams[x + 1] += count
            else:
                # No splitter: beams keep their column
                next_beams[x] += count

        beams = next_beams

    # After the last splitter row, beams just propagate straight down unchanged
    total_beams = sum(beams.values())
    return splits, total_beams


def part_one(grid: List[List[str]]) -> int:
    splits, _ = simulate(grid)
    return splits


def part_two(grid: List[List[str]]) -> int:
    _, total_beams = simulate(grid)
    return total_beams


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"
    grid = read_input()
    if arg == '1':
        print(part_one(grid))
    elif arg == '2':
        print(part_two(grid))
    else:
        print(part_one(grid))
        print(part_two(grid))


if __name__ == '__main__':
    main()
