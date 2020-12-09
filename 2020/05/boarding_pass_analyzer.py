import re
from typing import Dict

def read_input(path='input'):
    with open(path, 'r') as file:
        return [f.strip() for f in file.readlines()]


def get_row(row_sequence: str) -> int:
    upper = 128
    lower = 0
    for instruction in row_sequence:
        if instruction == 'F':
            upper -= (upper - lower) // 2
        elif instruction == 'B':
            lower += (upper - lower) // 2
    return min(lower, upper)


def get_col(col_sequence: str) -> int:
    upper = 8
    lower = 0
    for instruction in col_sequence:
        if instruction == 'R':
            lower += (upper - lower) // 2
        elif instruction == 'L':
            upper -= (upper - lower) // 2
    return min(lower, upper)


def find_seats(boarding_pass: str):
    p = re.compile(r'(?P<row>[BF]+)(?P<col>[LR]+)')
    matches = p.search(boarding_pass)
    row = get_row(matches.group('row'))
    col = get_col(matches.group('col'))
    return row, col


def find_seat_id(boarding_pass: str) -> int:
    row, col = find_seats(boarding_pass)
    return row * 8 + col


def find_all_seats(data):
    seats = {}
    for _ in data:
        row, col = find_seats(_)
        seats.setdefault(row, [])
        seats[row].append(col)
    return seats


def find_missing_seat(seats: Dict):
    seat_numbers = range(8)
    _ = sorted(seats.keys())[1:-1]
    for k in _:
        if len(seats[k]) < 8:
            for s in seat_numbers:
                if s not in seats[k]:
                    return k * 8 + s
            

if __name__ == "__main__":
    data = read_input()
    print(max([find_seat_id(_id) for _id in data]))
    print(find_missing_seat(find_all_seats(data)))
    