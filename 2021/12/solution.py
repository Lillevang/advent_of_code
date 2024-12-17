from collections import defaultdict
import sys


def read_input():
    connection_map = defaultdict(list)
    with open('./input', 'r') as file:
        for line in file.readlines():
            _ = line.strip().split('-')
            connection_map[_[0]].append(_[1])
            connection_map[_[1]].append(_[0])
    return connection_map


def part_one(connection_map: defaultdict) -> int:
    queue = [['start']]
    finished_paths = 0
    while queue:
        path = queue.pop(0)
        last_cave = path[-1]
        for next_cave in connection_map[last_cave]:
            if next_cave.islower() and next_cave in path:
                continue
            if next_cave == 'end':
                finished_paths += 1
                continue
            queue.append(path + [next_cave])
    return finished_paths


def part_two(connection_map: defaultdict) -> int:
    queue = [['start']]
    finished_paths = 0
    while queue:
        path = queue.pop(0)
        for next_cave in connection_map[path[-1]]:
            has_visited = next_cave.islower() and next_cave in path
            if next_cave == 'end':
                finished_paths += 1
            elif next_cave != 'start' and not (path[0] == '_' and has_visited):
                queue.append((['_'] if has_visited else []) + path + [next_cave])
    return finished_paths


def main() -> None:
    connection_map = read_input()
    if sys.argv[1] == '1':
        print(part_one(connection_map))
    elif sys.argv[1] == '2':
        print(part_two(connection_map))
    else:
        print(part_one(connection_map))
        print(part_two(connection_map))


if __name__ == '__main__':
    main()
