from typing import List
import sys

DIGIST_PER_BANK = 12


def read_input() -> List[str]:
    with open('./input', 'r') as file:
        return [[int(num) for num in bank] for bank in file.read().strip().splitlines()]


def max_joltage(bank):
    max_tens = max(bank[:-1])
    tens_index = bank.index(max_tens)

    max_ones = max(bank[tens_index + 1:])
    return 10 * max_tens + max_ones


def max_joltage_p2(bank):
    output: List[int] = []
    start_index = 0
    length = len(bank)

    for index in range(DIGIST_PER_BANK)[::-1]:
        window = bank[start_index: length - index]
        max_value = max(window)
        start_index = window.index(max_value) + start_index + 1
        output.append(max_value)

    return int("".join(str(num) for num in output))


def part_one(banks):
    return sum(max_joltage(bank) for bank in banks)


def part_two(banks):
    return sum(max_joltage_p2(bank) for bank in banks)


def main() -> None:
    data = read_input()
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == '1':
        print(part_one(data))
    elif arg == '2':
        print(part_two(data))
    else:
        print(part_one(data))
        print(part_two(data))


if __name__ == '__main__':
    main()
