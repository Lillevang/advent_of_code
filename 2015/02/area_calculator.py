import re
from typing import List
from functools import reduce

PATTERN = re.compile(r'(?P<length>\d+)x(?P<width>\d+)x(?P<height>\d+)')

def read_input(path='input') -> List:
    with open(path, 'r') as file:
        return [_.replace('\n', '') for _ in file.readlines()]
        

def calculate_area_of_box(length: int, width: int, height: int) -> int:
    return 2 * length * width + 2 * width * height + 2 * height * length


def find_smallest_side(length: int, width: int, height: int) -> int:
    l = sorted([length, width, height])[:2]
    return reduce((lambda x, y: x * y), l)
    

def calculate_volume_of_box(length: int, width: int, height: int) -> int:
    return length * width * height


def find_smallest_perimeter(length: int, width: int, height: int) -> int:
    l = sorted([length, width, height])[:2]
    return l[0] * 2 + l[1] * 2


def process_task_1(presents: List) -> int:
    total_area = 0
    for present in presents:
        matches = PATTERN.search(present)
        length = int(matches.group('length'))
        width = int(matches.group('width'))
        height = int(matches.group('height'))
        total_area += calculate_area_of_box(length, width, height)
        total_area += find_smallest_side(length, width, height)
    return total_area


def process_task_2(presents: List) -> int:
    total_ribbon = 0
    for present in presents:
        matches = PATTERN.search(present)
        length = int(matches.group('length'))
        width = int(matches.group('width'))
        height = int(matches.group('height'))
        total_ribbon += calculate_volume_of_box(length, width, height)
        total_ribbon += find_smallest_perimeter(length, width, height)
    return total_ribbon


if __name__ == "__main__":
    presents = read_input()
    print(process_task_1(presents))
    print(process_task_2(presents))