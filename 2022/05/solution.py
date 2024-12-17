from collections import defaultdict, deque
import re

def get_stacks():
    with open('input', 'r') as f:
        stacks, instructions = f.read().strip().split('\n\n')

    rows = stacks.split('\n')
    rows, stacks_row = rows[:-1], rows[-1]

    position_to_stack = {}
    stacks = defaultdict(deque)

    # Find stack positions
    position = 0
    while position < len(stacks_row):
        if stacks_row[position] != ' ':
            position_to_stack[stacks_row.index(stacks_row[position])] = stacks_row[position]
        position += 1

    for row in rows:
        position = 0
        while position < len(row):
            if position in position_to_stack and row[position] != ' ':
                stacks[position_to_stack[position]].appendleft(row[position])
            position += 1

    instructions = instructions.split('\n')

    return stacks, instructions

def part1():
    stacks, instructions = get_stacks()
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    for instruction in instructions:
        count, source, to = pattern.search(instruction).groups()
        i = 0
        while stacks[source] and i < int(count):
            stacks[to].append(stacks[source].pop())
            i += 1

    crates = [stacks[str(stack)].pop() for stack in range(1, 10)]
    print(f'Part 1: {"".join(crates)}')


def part2():
    stacks, instructions = get_stacks()
    pattern = re.compile(r'move (\d+) from (\d+) to (\d+)')
    for instruction in instructions:
        count, source, to = pattern.search(instruction).groups()
        i = 0
        tmp_crates = []
        while stacks[source] and i < int(count):
            tmp_crates.append(stacks[source].pop())
            i += 1

        for crate in reversed(tmp_crates):
            stacks[to].append(crate)

    crates = [stacks[str(stack)].pop() for stack in range(1, 10)]
    print(f'Part 2: {"".join(crates)}')

if __name__ == '__main__':
    part1() # Part 1: TBVFVDZPN
    part2() # Part 2: VLCWHTDSZ
