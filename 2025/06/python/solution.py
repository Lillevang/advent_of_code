from functools import reduce
from itertools import zip_longest
import sys
import operator

OPERATIONS = {"*": operator.mul, "+": operator.add}

# Token grid -> TODO: Add to utility templates, port to other language templates if possible


def read_input_part1():
    with open('./input', 'r') as file:
        for line in file:
            yield line.split()

# Character grid -> TODO: Add to utility templates, this is a nice approach!


def read_input_part2():
    with open('./input', 'r') as file:
        for line in file:
            yield list(line.rstrip("\n") + " ")


def parse(digits):
    s = ''.join(digits).strip()
    return None if not s else int(s)


def part_one(rows):
    total = 0
    for col in zip_longest(*rows):
        *nums, op_symbol = col
        op = OPERATIONS[op_symbol]
        digits = (int(n) for n in nums if n is not None)
        total += reduce(op, digits)
    return total


def part_two(rows):
    total = 0
    op = None
    digits = []

    for col in zip_longest(*rows, fillvalue=' '):
        data = list(col)
        key = data.pop()
        if key in OPERATIONS:
            op = OPERATIONS[key]

        value = parse(data)
        if value is not None:
            digits.append(value)
        else:
            if digits and op is not None:
                result = reduce(op, digits)
                total += result
                digits = []

    if digits and op is not None:
        total += reduce(op, digits)

    return total


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"

    if arg == '1':
        print(part_one(read_input_part1()))
    elif arg == '2':
        print(part_two(read_input_part2()))
    else:
        print(part_one(read_input_part1()))
        print(part_two(read_input_part2()))


if __name__ == '__main__':
    main()
