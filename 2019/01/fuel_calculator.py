from typing import List

def read_input(path='input'):
    with open(path, 'r') as file:
        return [int(_.strip()) for _ in file.readlines()]


def calculate_fuel_part_1(data: List[int]) -> int:
    fuel = 0
    for module in data:
        fuel += module // 3 - 2
    return fuel


def calculate_fuel_part_2(weight: int) -> int:
    fuel_req = max((weight // 3)- 2, 0)
    if fuel_req == 0:
        return 0
    return fuel_req + calculate_fuel_part_2(fuel_req)

if __name__ == "__main__":
    data = read_input()
    print('Part 1:', calculate_fuel_part_1(data))
    print('Part 2:', sum([calculate_fuel_part_2(_) for _ in data]))
