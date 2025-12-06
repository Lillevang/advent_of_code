from typing import List
import sys


def read_input() -> List[str]:
    with open('./input', 'r') as file:
        return file.readlines()


def parse_ranges(line: str):
    ranges = []
    for part in line.split(","):
        lo, hi = part.strip().split("-")
        ranges.append((int(lo), int(hi)))
    return ranges


def invalid_ids_in_range(lo: int, hi: int) -> List[int]:
    res = []
    s_lo = str(lo)
    s_hi = str(hi)
    min_digits = len(s_lo)
    max_digits = len(s_hi)

    for digits in range(min_digits, max_digits + 1):
        if digits % 2 == 1:
            continue

        half = digits // 2
        start = 10 ** (half - 1)
        end = 10 ** half

        for seed in range(start, end):
            x = int(str(seed) + str(seed))
            if x < lo:
                continue
            if x > hi:
                break
            res.append(x)

    return res


def invalid_ids_in_range_at_least_twice(lo: int, hi: int) -> List[int]:
    res = set()
    s_lo = str(lo)
    s_hi = str(hi)
    min_digits = len(s_lo)
    max_digits = len(s_hi)

    for digits in range(min_digits, max_digits + 1):
        for pattern_len in range(1, digits // 2 + 1):
            if digits % pattern_len != 0:
                continue
            repeats = digits // pattern_len
            if repeats < 2:
                continue

            start = 10 ** (pattern_len - 1)
            end = 10 ** pattern_len

            for seed in range(start, end):
                x = int(str(seed) * repeats)
                if x < lo:
                    continue
                if x > hi:
                    break
                res.add(x)

    return list(res)


def part_one(data: List[str]):
    line = data[0].strip()
    ranges = parse_ranges(line)
    total = 0
    for lo, hi in ranges:
        total += sum(invalid_ids_in_range(lo, hi))
    return total


def part_two(data: List[str]):
    line = data[0].strip()
    ranges = parse_ranges(line)
    total = 0
    for lo, hi in ranges:
        total += sum(invalid_ids_in_range_at_least_twice(lo, hi))
    return total


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
