from typing import List
import sys


def read_input() -> List[str]:
    with open('./input', 'r') as file:
        return file.readlines()


def part_one():
    raise NotImplementedError


def part_two():
    raise NotImplementedError


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
