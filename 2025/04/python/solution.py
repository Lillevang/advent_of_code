from typing import List
from collections import deque
import sys

NEIGHBORS = [
    (dr, dc)
    for dr in (-1, 0, 1)
    for dc in (-1, 0, 1)
    if not (dr == 0 and dc == 0)
]

Grid = list[list[str]]


def read_input() -> Grid:
    with open('./input', 'r') as file:
        return [list(line.strip()) for line in file if line.strip()]


def _count_neighbors_in_grid(grid: Grid, r: int, c: int) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    cnt = 0
    for dr, dc in NEIGHBORS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
            cnt += 1
    return cnt


def count_accessible_once(grid: Grid) -> int:
    return part_one(grid)


def part_one(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                if _count_neighbors_in_grid(grid, r, c) < 4:
                    total += 1
    return total


def part_two(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # present[r][c] = does this cell currently contain a roll?
    present: list[list[bool]] = [
        [grid[r][c] == "@" for c in range(cols)] for r in range(rows)
    ]

    # deg[r][c] = number of neighboring rolls
    deg: list[list[int]] = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if not present[r][c]:
                continue
            cnt = 0
            for dr, dc in NEIGHBORS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and present[nr][nc]:
                    cnt += 1
            deg[r][c] = cnt

    # queue of rolls that are currently accessible (< 4 neighbors)
    q: deque[tuple[int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if present[r][c] and deg[r][c] < 4:
                q.append((r, c))

    removed = 0
    while q:
        r, c = q.popleft()
        if not present[r][c]:
            continue  # might already have been removed via another path

        # Remove this roll
        present[r][c] = False
        removed += 1

        # Update neighbors
        for dr, dc in NEIGHBORS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and present[nr][nc]:
                deg[nr][nc] -= 1
                # It just transitioned from 4 → 3, so it becomes newly removable
                if deg[nr][nc] == 3:
                    q.append((nr, nc))
    return removed


def main() -> None:
    data = read_input()
    try:
        if sys.argv[1] == '1':
            print(part_one(data))
        elif sys.argv[1] == '2':
            print(part_two(data))
    except:
        print(part_one(data))
        print(part_two(data))


if __name__ == '__main__':
    main()
