from itertools import combinations


def read_input(path='input'):
    output = []
    with open(path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        output.append([int(num) for num in line.replace('\n', '').split('\t')])
    return output


def calculate_checksum_part_1(data):
    checksum = 0
    for line in data:
        checksum += max(line) - min(line)
    return checksum


def calculate_checksum_part_2(data):
    return sum(b//a for line in data for a, b in combinations(sorted(line), 2) if b % a == 0)


if __name__ == "__main__":
    data = read_input()
    print(calculate_checksum_part_1(data))
    print(calculate_checksum_part_2(data))
