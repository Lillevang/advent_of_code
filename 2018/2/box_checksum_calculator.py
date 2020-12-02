from collections import Counter
from typing import List
from itertools import combinations, compress

def read_input(path='input'):
    with open(path, 'r') as file:
        return [_.replace('\n', '') for _ in file]


def process_data_part_1(data: List[str]) -> int:
    twos = 0
    threes = 0
    for _id in data:
        _vals = Counter(_id).values()
        if 2 in _vals:
            twos += 1
        if 3 in _vals:
            threes += 1
    return twos * threes
          

def process_data_part_2(data: List[str]) -> int:
    for s1, s2 in combinations(data, 2):
        diff = [e1 == e2 for e1, e2 in zip(s1, s2)]
        if sum(diff) == (len(s1) - 1):
            res = ''.join(list(compress(s1, diff)))
            return res
    return None


if __name__ == "__main__":
    data = read_input()
    print(process_data_part_1(data))
    print(process_data_part_2(data))
