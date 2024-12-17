import sys
from typing import List


def read_input() -> List[str]:
    with open('./input', 'r') as file:
        return file.readlines()


def part_one(data: List[str]) -> int:    
    x = 0
    y = 0
    for l in data:
        _ = l.split(' ')
        n = int(_[1])
        if _[0] == 'up':
            y -= n
        elif _[0] == 'down':
            y += n
        else:
            x += n
    return x * y


def part_two(data: List[str]) -> int:
    x = 0
    y = 0
    aim = 0
    for l in data:
        _ = l.split(' ')
        n = int(_[1])
        if _[0] == 'up':
            aim -= n
        elif _[0] == 'down':
            aim += n
        else:
            x += n
            y += aim * n
    return x * y


def main() -> None:
    data = read_input()
    if sys.argv[1] == '1':
        print(part_one(data))
    elif sys.argv[1] == '2':
        print(part_two(data))
    else:
        print(part_one(data))
        print(part_two(data))


if __name__ == '__main__':
    main()
