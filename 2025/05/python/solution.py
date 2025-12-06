import sys
import bisect


def read_input(path: str = "input") -> tuple[list[tuple[int, int]], list[int]]:
    with open(path, "r") as f:
        blocks = f.read().strip().split("\n\n")

    range_lines = blocks[0].splitlines()
    id_lines = blocks[1].splitlines()

    ranges: list[tuple[int, int]] = []
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
    merged: list[tuple[int, int]] = []
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
    try:
        if sys.argv[1] == '1':
            print(part_one(ranges, ingredient_ids))
        elif sys.argv[1] == '2':
            print(part_two(ranges))
    except Exception:
        print("We fucked up...")


if __name__ == '__main__':
    main()
