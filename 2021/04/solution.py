from typing import List
import sys


class BingoBoard:

    def __init__(self, numbers: List[str]):
        self.rows_and_columns = numbers


    def create_board(self, numbers: List[str]) -> List[int]:
        for _ in numbers:
            [int(n) for n in _.strip().replace('  ', ' ').split(' ')]
        


    def has_bingo(self) -> bool:
        return [] in self.rows_and_columns


    def mark_number(self, number: int) -> None:
        for rc in self.rows_and_columns:
            if number in rc:
                rc.remove(rc)


def read_input():
    with open('./input', 'r') as file:
        numbers = file.readline().strip()
        file.readline()
        data = []
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i] == '\n':
                data.append(lines[i-5:i])
        return numbers, data


def part_one():
    raise NotImplementedError


def part_two():
    raise NotImplementedError


def main() -> None:
    numbers, data = read_input()
    print(len(data))
    try:
        if sys.argv[1] == '1':
            print(part_one(data))
        elif sys.argv[1] == '2':
            print(part_two(data))
    except IndexError:
        pass
        #print(part_one(data))
        #print(part_two(data))


if __name__ == '__main__':
    main()
