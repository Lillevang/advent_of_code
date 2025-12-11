from typing import Dict, List
import functools
import sys


def read_input() -> Dict[str, List[str]]:
    nodes = {}
    with open('./input', 'r') as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue

            left, right = line.split(": ")
            neighbors = right.split()
            nodes[left] = neighbors

    nodes.setdefault("out", [])
    return nodes


NODES = read_input()


@functools.cache
def paths(current: str, has_visited_dac: bool, has_visited_fft: bool) -> int:
    if current == "fft":
        has_visited_fft = True

    if current == "dac":
        has_visited_dac = True

    if current == "out":
        return 1 if has_visited_dac and has_visited_fft else 0

    return sum(
        paths(node, has_visited_dac, has_visited_fft)
        for node in NODES[current]
    )


def part_one() -> int:
    return paths("you", True, True)


def part_two() -> int:
    return paths("svr", False, False)


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"
    if arg == '1':
        print(part_one())
    elif arg == '2':
        print(part_two())
    else:
        print(part_one())
        print(part_two())


if __name__ == '__main__':
    main()
