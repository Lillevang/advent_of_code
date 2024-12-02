import sys
from typing import List
from functools import reduce
from statistics import median


bs = {"(": ")", "[": "]", "{": "}", "<": ">"}
d1 = {")": 3, "]": 57, "}": 1197, ">": 25137}
d2 = {"(": 1, "[": 2, "{": 3, "<": 4}


def read_input() -> List[str]:
    with open('input') as file:
        return [x.strip() for x in file]


def part_one(data: List[str]) -> int:
    _ = []
    for line in data:
        stack = []
        for c in line:
            if c in '<{[(':
                stack.append(c)
            else:
                if bs[stack.pop()] != c:
                    _.append(d1[c])
                    break
    return sum(_)


def part_two(data: List[str]) -> int:
    _ = []
    for line in data:
        stack = []
        for c in line:
            if c in '<{[(':
                stack.append(c)
            else:
                if bs[stack.pop()] != c:
                    break
        else:
            _.append(reduce(lambda x, y: x*5 + d2[y], stack[::-1], 0))
    return median(_)


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
