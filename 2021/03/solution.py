from typing import List, Dict, Tuple
import sys


def read_input() -> List[str]:
    with open('./input', 'r') as file:
        return [_.strip() for _ in file.readlines()]


def construct_binaries(bin_len: int, data: Dict[int, Dict[str, int]]) -> Tuple[str, str]:
    gamma = ''
    epsilon = ''
    for i in range(bin_len):
        gamma += max(data[i], key=data[i].get)
        epsilon += min(data[i], key=data[i].get)
    return (gamma, epsilon)


def create_index_dict(bin_len: int, data: List[str]) -> Dict[int, Dict[str, int]]:
    index_dict = {}
    for _ in data:
        for i in range(bin_len):
            index_dict.setdefault(i, {'0': 0, '1': 0})
            index_dict[i][_[i]] += 1
    return index_dict


def filter_bins(bins: List[str], index: int, is_oxy = True) -> List[str]:
    if len(bins) == 1:
        return bins
    cols = list(zip(*bins))
    current_col = cols[index]
    if is_oxy:
        key = '1' if current_col.count('1') >= current_col.count('0') else '0'
    else:
        key = '1' if current_col.count('0') > current_col.count('1') else '0'
    return [n for n in bins if n[index] == key]


def part_one(data: List[str]) -> int:
    # 1029192
    bin_len = len(data[0]) - 1
    index_dict = create_index_dict(bin_len, data)
    binaries = construct_binaries(bin_len, index_dict)
    return int(binaries[0], 2) * int(binaries[1], 2)


def part_two(data: List[str]) -> int:
    # 3832770
    oxy_bins = data.copy()
    co2_bins = data.copy()
    for i in range(len(data[0])):
        oxy_bins = filter_bins(oxy_bins, i)
        co2_bins = filter_bins(co2_bins, i, is_oxy = False)
        if len(oxy_bins) == 1 and len(co2_bins) == 1:
            return int(oxy_bins[0], 2) * int(co2_bins[0], 2)
    raise RuntimeError


def main() -> None:
    data = read_input()
    if sys.argv[1] == '1':
        print(part_one(data))
    elif sys.argv[1] == '2':
        print(part_two(data))
    else:
        print(part_one(data))
        print(part_two(data))


if __name__ == '__main__':
    main()
