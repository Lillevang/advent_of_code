import sys
import bisect
from typing import List, Tuple

Range = Tuple[int, int]


def read_input(path: str = "input") -> tuple[List[Range], List[int]]:
    with open(path, "r") as f:
        blocks = f.read().strip().split("\n\n")

    range_lines = blocks[0].splitlines()
    id_lines = blocks[1].splitlines()

    ranges: List[Range] = []
    for line in range_lines:
        line = line.strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        ranges.append((int(start_str), int(end_str)))

    ingredient_ids = [int(line.strip()) for line in id_lines if line.strip()]

    return ranges, ingredient_ids


def merge_ranges(ranges):
    if not ranges:
        return []

    # sort by start
    ranges = sorted(ranges, key=lambda r: r[0])
    merged: List[Range] = []
    cur_start, cur_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= cur_end + 1:
            # overlap or directly adjacent -> merge
            cur_end = max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    merged.append((cur_start, cur_end))
    return merged


def part_one(ranges, ingredient_ids) -> int:
    merged = merge_ranges(ranges)

    # Prepare arrays for binary search
    starts = [s for (s, _) in merged]
    ends = [e for (_, e) in merged]

    fresh_count = 0

    for x in ingredient_ids:
        # Find rightmost range whose start <= x
        idx = bisect.bisect_right(starts, x) - 1
        if idx >= 0 and ends[idx] >= x:
            # x is within merged[idx]
            fresh_count += 1

    return fresh_count


def part_two(ranges) -> int:
    merged = merge_ranges(ranges)
    return sum(end - start + 1 for start, end in merged)


def main() -> None:
    ranges, ingredient_ids = read_input()
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == '1':
        print(part_one(ranges, ingredient_ids))
    elif arg == '2':
        print(part_two(ranges))
    else:
        print(part_one(ranges, ingredient_ids))
        print(part_two(ranges))


if __name__ == '__main__':
    main()
