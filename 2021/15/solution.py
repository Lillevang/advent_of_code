import sys
import numpy as np
import heapq


def read_input():
    map = np.genfromtxt("input", dtype=int, delimiter=1)
    height, width = map.shape
    return height, width

def neighbors(x, y, scale, width, height):
    out = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(a, b) for a, b in out if 0 <= a < width * scale and 0 <= b < height * scale]

def cost(x, y, width, height):  
    c = map[y % height, x % width]
    c = c + x // width + y // height
    c = 1 + (c-1) % 9
    return c

def dijkstra(scale : int, width, height):
    distances = {(0,0):0}
    pq = [(0, (0,0))]
    while len(pq) > 0:
        total, (x,y) = heapq.heappop(pq)
        if total <= distances[(x, y)]:
            for n in neighbors(x, y, scale, width, height):
                distance = total + cost(*n, width, height)
                if distance < distances.get(n, 1e308):
                    distances[n] = distance
                    heapq.heappush(pq, (distance, n))

    return distances[(width*scale-1, height*scale-1)]

def part_one():
    height, width = read_input()
    print(dijkstra(1, width, height))

def part_two():
    height, width = read_input()
    print(dijkstra(5, width, height))

def main() -> None:
    data = read_input()
    try:
        if sys.argv[1] == '1':
            part_one(data)
        elif sys.argv[1] == '2':
            part_two(data)
    except:
        part_one(data)
        part_two(data)


if __name__ == '__main__':
    main()
