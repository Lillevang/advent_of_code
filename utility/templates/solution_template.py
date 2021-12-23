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
