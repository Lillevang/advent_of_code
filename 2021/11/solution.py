from typing import Dict, Tuple
import sys
import itertools as it


def read_input() -> Dict[Tuple[int, int], int]:
    with open('./input', 'r') as file:
        return {
            (x, y) : int(energy)
                for y, ln in enumerate(file.readlines())
                for x, energy in enumerate(ln) if energy != '\n'
        }    


def evolve(octopuses: Dict[Tuple[int, int], int]):
    for (x, y), energy in octopuses.items():
        octopuses[x, y] += 1

    flashed = set()
    while any(
        (x, y) not in flashed and energy > 9
        for (x, y), energy in octopuses.items()
    ):
        for (x, y), energy in octopuses.items():
            if (energy > 9) and ((x,y) not in  flashed):
                flashed.add((x,y))

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (x + dx, y + dy) in octopuses.keys():
                            octopuses[x + dx, y + dy] += 1
        for (x, y) in flashed:
            octopuses[x, y] = 0
    return len(flashed)


def part_one(octopuses: Dict[Tuple[int, int], int]) -> int:
    flashes = 0
    for _ in range(1, 101):
        flashes = flashes + evolve(octopuses)
    return flashes


def part_two(octopuses: Dict[Tuple[int, int], int]) -> int:
    flashes = 0
    for _ in range(1, 101):
        flashes = flashes + evolve(octopuses)
    
    for _ in it.count(_):
        if evolve(octopuses) >= len(octopuses.keys()):
            return _ + 1


def main() -> None:
    octopuses = read_input()
    if sys.argv[1] == '1':
        print(part_one(octopuses))
    elif sys.argv[1] == '2':
        print(part_two(octopuses))
    else:
        print(part_one(octopuses))
        print(part_two(octopuses))


if __name__ == '__main__':
    main()
