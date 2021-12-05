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
    for i in range(bin_len):
        index_dict.setdefault(i, {'0': 0, '1': 0})
    for l in data:
        _ = l
        for i in range(bin_len):
            index_dict[i][_[i]] += 1
    return index_dict


def get_bin_rating(data) -> int:
    oxy_bins = data.copy()
    co2_bins = data.copy()
    for i in range(len(data[0])):
        if len(co2_bins) > 1:
            co2_cols = list(zip(*co2_bins))
            current_co2_col = co2_cols[i]
            co2_key = '0'
            if current_co2_col.count('0') > current_co2_col.count('1'):
                co2_key = '1'
            co2_bins = [n for n in co2_bins if n[i] == co2_key]

        if len(oxy_bins) > 1:
            oxy_cols = list(zip(*oxy_bins))
            current_oxy_col = oxy_cols[i]
            oxy_key = '0'
            if current_oxy_col.count('1') >= current_oxy_col.count('0'):
                oxy_key = '1'
            oxy_bins = [n for n in oxy_bins if n[i] == oxy_key]
        if len(oxy_bins) == 1 and len(co2_bins) == 1:
            return int(oxy_bins[0], 2) * int(co2_bins[0], 2)
    return None


def part_one(data: List[str]) -> int:
    # 1029192
    bin_len = len(data[0]) - 1
    index_dict = create_index_dict(bin_len, data)
    binaries = construct_binaries(bin_len, index_dict)
    return int(binaries[0], 2) * int(binaries[1], 2)


def part_two(data: List[str]) -> int:
    # 3832770
    return get_bin_rating(data)


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
