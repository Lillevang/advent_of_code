from typing import List, Dict
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
        self.is_horizontal = self.e1.x == self.e2.x
        self.is_vertical = self.e1.y == self.e2.y
        self.is_horizontal_or_vertical = self.is_horizontal or self.is_vertical
        self.points_on_line = self.find_points_on_line()


    def find_points_on_line(self) -> List[str]: # Only horizontal or vertical lines
        points_on_line = []
        if self.is_vertical:
            direction = 1 if self.e1.x < self.e2.x else -1
            for i in range(self.e1.x, self.e2.x + direction, direction):
                points_on_line.append(f'{i},{self.e1.y}')
        elif self.is_horizontal:
            direction = 1 if self.e1.y < self.e2.y else -1
            for i in range(self.e1.y, self.e2.y + direction, direction):
                points_on_line.append(f'{self.e1.x},{i}')
        return points_on_line


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

def get_all_points() -> Dict[str, int]:
    points = {}
    for i in range(1000):
        for j in range(1000):
            points[f'{i},{j}'] = 0
    return points


def part_one(lines: List[Line]):
    points = get_all_points()
    for line in lines:
        for point in line.points_on_line:
            points[point] += 1
    return sum([_ for _ in points.values() if _ >= 2])


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
