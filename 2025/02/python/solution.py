from typing import List, Tuple
import sys


def read_input() -> List[str]:
    with open("./input", "r") as file:
        return file.readlines()


def parse_ranges(line: str) -> List[Tuple[int, int]]:
    ranges: List[Tuple[int, int]] = []
    for part in line.split(","):
        lo_str, hi_str = part.strip().split("-")
        ranges.append((int(lo_str), int(hi_str)))
    return ranges


def invalid_ids_in_range(lo: int, hi: int) -> List[int]:
    res: List[int] = []
    s_lo = str(lo)
    s_hi = str(hi)
    min_digits = len(s_lo)
    max_digits = len(s_hi)

    for digits in range(min_digits, max_digits + 1):
        # Only even digit counts can be split into two equal halves
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
        # pattern_len is the length of the base pattern that gets repeated
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


def part_one(data: List[str]) -> int:
    line = data[0].strip()
    ranges = parse_ranges(line)
    total = 0
    for lo, hi in ranges:
        total += sum(invalid_ids_in_range(lo, hi))
    return total


def part_two(data: List[str]) -> int:
    line = data[0].strip()
    ranges = parse_ranges(line)
    total = 0
    for lo, hi in ranges:
        total += sum(invalid_ids_in_range_at_least_twice(lo, hi))
    return total


def main() -> None:
    data = read_input()
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    if arg == "1":
        print(part_one(data))
    elif arg == "2":
        print(part_two(data))
    else:
        # Default: run both parts, like your original fallback
        print(part_one(data))
        print(part_two(data))


if __name__ == "__main__":
    main()
