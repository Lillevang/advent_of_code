from typing import List
import sys


class BingoBoard:

    def __init__(self, numbers):
        self.sum_of_numbers = 0
        self.rows = self.create_rows(numbers)
        self.columns = self.create_columns(self.rows)
        self.has_bingo = False

    def create_columns(self, rows):
        cols = []
        for c in list(zip(*self.rows)):
            new_col = []
            for i in c:
                new_col.append(i)
            cols.append(new_col)
        return cols

    def create_rows(self, numbers):
        rows = []
        for r in numbers:
            row = []
            for _ in r:
                row.append(int(_))
            rows.append(row)
            self.sum_of_numbers += sum(row)
        return rows

    def check_bingo(self) -> None:
        self.has_bingo = [] in self.rows or [] in self.columns

    def mark_number(self, number: int) -> None:
        if self.has_bingo:
            return
        number_found = False
        for r in self.rows:
            if number in r:
                r.remove(number)
                number_found = True
        for c in self.columns:
            if number in c:
                c.remove(number)
                number_found = True
        if number_found:
            self.sum_of_numbers -= number
        self.check_bingo()


def read_input():
    with open('./input', 'r') as file:
        numbers = [int(_) for _ in file.readline().strip().split(',')]
        file.readline()
        boards = []
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i] == '\n':
                board_input = []
                for l in lines[i-5:i]:
                    board_input.append([_ for _ in l.strip().replace('  ', ' ').split(' ')])
                boards.append(BingoBoard(board_input))
        return numbers, boards


def part_one(numbers: List[int], boards: List[BingoBoard]) -> int:
    for n in numbers:
        for b in boards:
            b.mark_number(n)
            if b.has_bingo:
                return b.sum_of_numbers * n
    raise RuntimeError


def part_two(numbers: List[int], boards: List[BingoBoard]) -> int:
    remaining_boards = [_ for _ in boards if not _.has_bingo]
    last_board = None
    for n in numbers:
        for b in boards:
            b.mark_number(n)
            remaining_boards = [_ for _ in boards if not _.has_bingo]
        if len(remaining_boards) == 1:
            last_board = remaining_boards[0]
        if last_board and last_board.has_bingo:
            return last_board.sum_of_numbers * n
    raise RuntimeError


def main() -> None:
    numbers, boards = read_input()
    try:
        if sys.argv[1] == '1':
            print(part_one(numbers, boards))
        elif sys.argv[1] == '2':
            print(part_two(numbers, boards))
    except IndexError:
        print(part_one(numbers, boards))
        print(part_two(numbers, boards))


if __name__ == '__main__':
    main()
