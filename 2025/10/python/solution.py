from collections import defaultdict
from typing import List
from z3 import Int, Optimize
import sys


def read_input() -> List[str]:
    rows = []
    with open('./input', 'r') as file:
        for line in file:
            parts = line.strip().split(" ")
            lights_raw = parts[0]
            wiring = parts[1:-1]
            joltage_raw = parts[-1]
            lights = [ch == "#" for ch in lights_raw[1:-1]]
            start_indices = [i for i, on in enumerate(lights) if on]
            end = [int(num) for num in joltage_raw[1:-1].split(",")]
            rows.append((wiring, end, start_indices))

    return rows


def to_bitmask(x):
    y = 0
    for i in x:
        y += 2**i
    return y


def from_bitmask(x, n):
    y = []
    for i in range(n):
        if x % 2 == 1:
            y.append(i)
        x //= 2
    return y


def part_one(rows):
    ret = 0

    for wiring, end, start_indices in rows:

        # parse buttons for this line
        buttons = [[int(x) for x in wire[1:-1].split(",")] for wire in wiring]

        start = to_bitmask(start_indices)
        buttons_masks = [to_bitmask(x) for x in buttons]
        end_mask = 0

        current = {start}
        iterations = 0

        while end_mask not in current:
            nx = set()
            for c in current:
                for button in buttons_masks:
                    nx.add(c ^ button)
            current = nx
            iterations += 1

        ret += iterations

    return ret


def part_two(rows):
    total_presses = 0
    for wiring, end, start_indices in rows:
        buttons = [[int(x) for x in wire[1:-1].split(",")] for wire in wiring]
        presses = Int("presses")
        button_vars = [Int(f"button{i}") for i in range(len(buttons))]

        counters_to_buttons = defaultdict(list)
        for i, button in enumerate(buttons):
            for flip in button:
                counters_to_buttons[flip].append(i)

        equations = []

        # For each light index, enforce a target count
        for counter, counter_buttons in counters_to_buttons.items():
            equations.append(end[counter] == sum(button_vars[i]
                             for i in counter_buttons))

        # Non-negativity on button presse
        for button_var in button_vars:
            equations.append(button_var >= 0)

        equations.append(presses == sum(button_vars))

        opt = Optimize()
        opt.add(equations)
        opt.minimize(presses)
        res = opt.check()
        if str(res) != "sat":
            raise RuntimeError(f"Unknown model for line {res}")

        model = opt.model()
        output = model[presses]
        total_presses += int(str(output))

    return total_presses


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"
    rows = read_input()
    if arg == '1':
        print(part_one(rows))
    elif arg == '2':
        print(part_two(rows))
    else:
        print(part_one(rows))
        print(part_two(rows))


if __name__ == '__main__':
    main()
