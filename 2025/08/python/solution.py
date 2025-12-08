from typing import List, Tuple
from dataclasses import dataclass
import sys


@dataclass
class Point3D:
    x: int
    y: int
    z: int


class DSU:
    """Disjoint Set Union / Union-Find with union by size and path compression."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """Union sets containing a and b. Return True if merged, False if already same set."""
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def read_input(path="input") -> List[Point3D]:
    points: List[Point3D] = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str, z_str = line.split(",")
            points.append(Point3D(int(x_str), int(y_str), int(z_str)))
    return points


def squared_distance(a: Point3D, b: Point3D) -> int:
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return dx * dx + dy * dy + dz * dz


def part_one(points: List[Point3D], k: int) -> int:
    n = len(points)
    dsu = DSU(n)

    # Build all edges (dist2, i, j)
    edges: List[Tuple[int, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            dist2 = squared_distance(points[i], points[j])
            edges.append((dist2, i, j))

    # Sort by distance
    edges.sort(key=lambda e: e[0])

    # Process the K shortest edges
    for idx, (_, u, v) in enumerate(edges):
        if idx == k:
            break
        # Attempt to connect; if already in same circuit, nothing happens
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)

    # Compute component sizes
    comp_sizes = {}
    for i in range(n):
        root = dsu.find(i)
        comp_sizes[root] = comp_sizes.get(root, 0) + 1

    sizes = sorted(comp_sizes.values(), reverse=True)
    # Puzzle will guarantee at least three circuits; if not, pad with 1s
    while len(sizes) < 3:
        sizes.append(1)

    return sizes[0] * sizes[1] * sizes[2]


def part_two(points: List[Point3D]) -> int:
    n = len(points)
    if n < 2:
        raise ValueError(f"Need at least 2 junction boxes, got {n}")
    dsu = DSU(n)

    # Build all edges (dist2, i, j)
    edges: List[Tuple[int, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            dist2 = squared_distance(points[i], points[j])
            edges.append((dist2, i, j))

    edges.sort(key=lambda e: e[0])

    components = n
    last_u = last_v = None

    for _, u, v in edges:
        if dsu.union(u, v):
            components -= 1
            last_u, last_v = u, v
            if components == 1:
                break

    if last_u is None or last_v is None:
        raise RuntimeError("Graph was already connected or had <= 1 node")

    return points[last_u].x * points[last_v].x


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"
    data = read_input("input")  # swap to "input" for real run
    if arg == "1":
        print(part_one(data, 1000))   # adjust k as needed
    elif arg == "2":
        print(part_two(data))
    else:
        print(part_one(data, 1000))
        print(part_two(data))


if __name__ == "__main__":
    main()
