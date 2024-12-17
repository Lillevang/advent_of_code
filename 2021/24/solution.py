from typing import List
import sys
from z3 import Optimize, And, Int, If, sat

# Input data repeats except for the parameters on line: 4, 5 and 15. These are cached.
def read_input() -> List[List[int]]:
    with open('./input', 'r') as file:
        lines = file.readlines()
        return [[int(y.split()[-1]) for y in [lines[i + 4], lines[i + 5], lines[i + 15]]] for i in range(0, len(lines), 18)]


def solve(max, lines: List[List[int]]) -> int:
    # z3 is used for optimizing the decompiled program.
    s = Optimize()
    z = 0 # running z. Has to be 0 at the start
    v = 0 # concatenating digits is stored in this variable
    for (i,  [p, q, r]) in enumerate(lines):
        w = Int(f'w{i}')
        v = v * 10 + w # Concatenating the values
        s.add(And(w >= 1, w <= 9)) # the check for valid digits (1-9) is added to the optimizer
        z = If(z % 26 + q == w, z / p, z/p * 26 +  w + r) # The repeated sequence is decompiled into these operations. 
    s.add(z == 0)

    (s.maximize if max else s.minimize)(v)
    assert s.check() == sat
    return s.model().eval(v)


def part_one(data: List[List[int]]) -> None:
    print(solve(True, data))


def part_two(data: List[List[int]]) -> None:
    print(solve(False, data))


def main() -> None:
    data = read_input()
    try:
        if sys.argv[1] == '1':
            part_one(data)
        elif sys.argv[1] == '2':
            part_two(data)
    except IndexError:
        part_one(data)
        part_two(data)


if __name__ == '__main__':
    main()
