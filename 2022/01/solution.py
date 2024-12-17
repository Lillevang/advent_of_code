
with open('./input', 'r') as file:
    elf_supplies = [sum(int(x) for x in line.split()) for line in file.read().split('\n\n')]

# Part 1
print(f'Part 1: {max(elf_supplies)}')

# Part 2
print(f'Part 2: {sum(sorted(elf_supplies)[-3:])}')
