import numpy as np
import sys

from numpy.core.fromnumeric import reshape
sys.path.insert(1,'../../utility')
from typing import List
from grid_padder import GridPadder
from collections import Counter
from skimage import measure


def read_input() -> List[List[int]]:
    output = []
    with open('./input', 'r') as file:
        for line in file.readlines():
            _ = []
            for c in line.strip():
                _.append(int(c))
            output.append(_)
    gridPadder = GridPadder[int](output, 9)
    return gridPadder.pad_grid(output, 9)



def part_one(padded_grid: List[List[int]]) -> int:
    low_points = []
    for i in range(1, len(padded_grid) - 1):
        for j in range(1, len(padded_grid[0]) - 1):
            cur_num = padded_grid[i][j]
            above = padded_grid[i-1][j]
            below = padded_grid[i+1][j]
            left = padded_grid[i][j-1]
            right = padded_grid[i][j+1]
            if  cur_num < above and cur_num < below and cur_num < left and cur_num < right:
                low_points.append(1 + cur_num)
    return sum(low_points)


def part_two() -> int:
    data = []
    with open('input', 'r') as file:
        for line in file.readlines():
            data.append(list(line.strip()))
    
    a = np.array(data).astype(np.int32)
    b = a != 9
    c = b.astype(int)
    d = measure.label(c, connectivity=1)
    count = Counter()
    for x in range(np.max(d))[1:]:
        count[x] = np.count_nonzero(d == x)
    basins = count.most_common(3)
    result = 1
    for x in basins:
        result = result * x[1]

    return result


def main() -> None:
    padded_grid = read_input()
    if sys.argv[1] == '1':
        print(part_one(padded_grid))
    elif sys.argv[1] == '2':
        print(part_two())
    else:
        print(part_one(padded_grid))
        print(part_two())


if __name__ == '__main__':
    main()