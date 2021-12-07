from typing import List, Set
import sys


class Point:
        
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.lines_passing_through_ctr = 0


class Line:

    def __init__(self, ends: List[Point]) -> None:
        self.e1 = ends[0]
        self.e2 = ends[1]
        self.is_horizontal_or_vertical = self.e1.x == self.e2.x or self.e1.y == self.e2.y


class GeothermicVentMap:

    def __init__(self, lines: List[Line]) -> None:
        self.points = []
        self.lines = lines
        self.add_points()
        self.process_data(lines)

    def process_data(self, lines: List[Line]) -> None:
        for line in lines:
            pass

    def add_points(self):
        for i in range(1000):
            for j in range(1000):
                self.points.append(Point(i,j))


def read_input() -> List[Line]:
    with open('./input', 'r') as file:
        lines = []
        for l in file.readlines():
            line_ends = []
            for _ in l.strip().split(' -> '):
                coordinate = _.split(',')
                line_ends.append(Point(int(coordinate[0]), int(coordinate[1])))
            lines.append(Line(line_ends))
        return lines

def part_one(lines: List[Line]):
    geothermic_vent_map = GeothermicVentMap([_ for _ in lines if _.is_horizontal_or_vertical])


def part_two(lines):
    raise NotImplementedError


def main() -> None:
    lines = read_input()
    try:
        if sys.argv[1] == '1':
            print(part_one(lines))
        elif sys.argv[1] == '2':
            print(part_two(lines))
        elif sys.argv[1] == 'test':
            print()
    except IndexError:
        print(part_one(lines))
        print(part_two(lines))


if __name__ == '__main__':
    main()
