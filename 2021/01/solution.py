from typing import List
import sys

def read_input() -> List[int]:
    with open('./input', 'r') as file:
        return [int(_.strip()) for _ in file.readlines()]

def part_one(data: List[int]):
    
    prev_reading = data[0]
    increased = 0
    decreased = 0

    for reading in data[1:]:
        if reading > prev_reading:
            increased += 1
        else:
            decreased += 1
        prev_reading = reading

    print(increased)


def part_two(data: List[int]):
    prev_reading = sum(data[0:3])
    increased = 0
    decreased = 0
    equal = 0
    for i in range(2, len(data) - 1):
        cur_reading = sum(data[i-1:i+2])
        if cur_reading > prev_reading:
            increased += 1
        elif cur_reading < prev_reading:
            decreased += 1
        else:
            equal += 1
        prev_reading = cur_reading
    print(increased)


def main():
    data = read_input()
    if sys.argv[1] == '1':
        part_one(data)
    elif sys.argv[1] == '2':
        part_two(data)
    else:
        part_one(data)
        part_two(data)


if __name__ == '__main__':
    main()
