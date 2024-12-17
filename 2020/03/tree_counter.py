from functools import reduce

TREE = '#'

def read_input(path='input'):
    with open(path, 'r') as file:
        return [_.strip() for _ in file.readlines()]


def part_one(tree_map: list, slope_right: int, slope_down) -> int:
  return _count_trees(tree_map=tree_map,
                      slope_right=slope_right, slope_down=slope_down)


def part_two(tree_map: list, slopes: list):
  return reduce(
      lambda x, y: x * y,
      [_count_trees(tree_map=tree_map,
                    slope_right=slope[0],
                    slope_down=slope[1]) for slope in slopes],
      1)


def _count_trees(tree_map: list, slope_right: int, slope_down: int) -> int:
  num_trees = 0
  x = 0
  WIDTH = len(tree_map[0])

  for y in range(0, len(tree_map), slope_down):
    if tree_map[y][x % WIDTH] == TREE:
      num_trees += 1
    x += slope_right
  return num_trees

if __name__ == "__main__":
    data = read_input()
    print(part_one(data, 3, 1))
    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    print(part_two(data, slopes))
