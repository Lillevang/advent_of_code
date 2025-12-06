from typing import List
import sys


def read_input() -> List[str]:
    with open('./input_small', 'r') as file:
        return [[int(num) for num in bank] for bank in file.read().strip().splitlines()]


def max_joltage(bank):
    max_tens = max(bank[:-1])
    index = bank.index(max_tens)
    max_ones = max(bank[index+1:])
    return 10*max_tens+max_ones


def max_joltage_p2(bank):
    output = []
    start_index = 0
    length = len(bank)
    for index in range(12)[::-1]:
        max_value = max(bank[start_index:length-index])
        start_index = bank[start_index:length -
                           index].index(max_value)+start_index+1
        output.append(max_value)
    return int(''.join(str(num) for num in output))


def part_one(banks):
    return sum(max_joltage(bank) for bank in banks)


def part_two(banks):
    return sum(max_joltage_p2(bank) for bank in banks)


def main() -> None:
    data = read_input()
    try:
        if sys.argv[1] == '1':
            print(part_one(data))
        elif sys.argv[1] == '2':
            print(part_two(data))
    except Exception:
        print(part_one(data))
        print(part_two(data))


if __name__ == '__main__':
    main()
