from itertools import combinations
from typing import List, Tuple
import sys


Point = Tuple[int, int]


def read_input() -> List[str]:
    points: List[Point] = []
    with open('./input', 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            x_str, y_str = line.split(",")
            points.append((int(x_str), int(y_str)))
    return points


def part_one(points: List[Point]) -> int:
    max_area = 0
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[:i]:
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            if area > max_area:
                max_area = area
    return max_area


def compress_coordinates(points: List[Point]):
    xs: set[int] = set()
    ys: set[int] = set()

    for x, y in points:
        xs.add(x)
        xs.add(x + 1)
        ys.add(y)
        ys.add(y + 1)

    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)

    x_index = {x: i for i, x in enumerate(xs_sorted)}
    y_index = {y: i for i, y in enumerate(ys_sorted)}

    return xs_sorted, ys_sorted, x_index, y_index


def build_edge_grid(
    points: List[Point],
    indexed_points: List[Tuple[int, int]],
    nx: int,
    ny: int,
) -> List[List[int]]:
    # Bit flags for scanline parity
    ENTER = 1
    EXIT = 2
    CROSS = ENTER | EXIT  # 3

    grid = [[0] * ny for _ in range(nx)]
    n = len(points)

    for i in range(n):
        x1_idx, y1_idx = indexed_points[i]
        x2_idx, y2_idx = indexed_points[(i + 1) % n]

        # We only handle horizontal edges (x changes, y constant)
        if x1_idx != x2_idx:
            assert y1_idx == y2_idx
            if x1_idx > x2_idx:
                x1_idx, x2_idx = x2_idx, x1_idx

            # Mark entry/exit at endpoints and crossing in between
            grid[x1_idx][y1_idx] |= ENTER
            grid[x2_idx][y1_idx] |= EXIT
            for x in range(x1_idx + 1, x2_idx):
                grid[x][y1_idx] |= CROSS

    return grid


def scanline_fill(grid: List[List[int]]) -> List[List[bool]]:
    nx = len(grid)
    ny = len(grid[0]) if nx > 0 else 0

    filled = [[False] * ny for _ in range(nx)]

    for x_idx, row in enumerate(grid):
        parity = 0
        for y_idx, cell in enumerate(row):
            # We're inside if parity is non-zero or on an edge cell.
            filled[x_idx][y_idx] = (parity > 0) or (cell > 0)
            parity ^= cell
        # Polygon should be closed: parity back to 0 at row end
        assert parity == 0, (x_idx, row)

    return filled


def build_prefix_sums(mask: List[List[bool]]) -> List[List[int]]:
    nx = len(mask)
    ny = len(mask[0]) if nx > 0 else 0

    prefix = [[0] * (ny + 1) for _ in range(nx + 1)]

    for x in range(nx):
        for y in range(ny):
            prefix[x + 1][y + 1] = (
                int(mask[x][y])
                + prefix[x][y + 1]
                + prefix[x + 1][y]
                - prefix[x][y]
            )

    return prefix


def rect_sum(
    prefix: List[List[int]],
    x1: int,
    y1: int,
    x2: int,
    y2: int
) -> int:
    return (
        prefix[x2 + 1][y2 + 1]
        - prefix[x1][y2 + 1]
        - prefix[x2 + 1][y1]
        + prefix[x1][y1]
    )


def part_two(points: List[Point]) -> int:
    # Coordinate compression
    xs, ys, x_index, y_index = compress_coordinates(points)
    nx, ny = len(xs), len(ys)

    # Precompute point indices in the compressed grid
    indexed_points = [(x_index[x], y_index[y]) for (x, y) in points]

    # 1) Build edge grid from polygon edges
    edge_grid = build_edge_grid(points, indexed_points, nx, ny)

    # 2) Fill interior (and border) using scanline
    inside_grid = scanline_fill(edge_grid)

    # 3) Build prefix sums to allow O(1) area queries
    prefix = build_prefix_sums(inside_grid)

    # 4) Try all rectangles defined by pairs of original points and
    #    keep only those fully inside the polygon.

    point_to_idx = {pt: (x_index[pt[0]], y_index[pt[1]]) for pt in points}
    max_area = 0

    for p1, p2 in combinations(points, 2):
        x1, y1 = p1
        x2, y2 = p2

        # Get compressed indices
        ix1, iy1 = point_to_idx[p1]
        ix2, iy2 = point_to_idx[p2]

        # Sorting creates the bounding box
        ox_min, ox_max = (x1, x2) if ix1 < ix2 else (x2, x1)
        oy_min, oy_max = (y1, y2) if y1 < y2 else (y2, y1)

        cx_min, cx_max = (ix1, ix2) if ix1 < ix2 else (ix2, ix1)
        cy_min, cy_max = (iy1, iy2) if iy1 < iy2 else (iy2, iy1)

        # Check area validity
        good_cells = rect_sum(prefix, cx_min, cy_min, cx_max, cy_max)
        total_cells = (cx_max - cx_min + 1) * (cy_max - cy_min + 1)

        if good_cells == total_cells:
            width = ox_max - ox_min + 1
            height = oy_max - oy_min + 1
            max_area = max(max_area, width * height)
    return max_area


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"
    data = read_input()
    if arg == '1':
        print(part_one(data))
    elif arg == '2':
        print(part_two(data))
    else:
        print(part_one(data))
        print(part_two(data))


if __name__ == '__main__':
    main()
