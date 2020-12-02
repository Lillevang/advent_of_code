
def read_input(path='input'):
    out = []
    with open(path, 'r') as file:
        for line in file:
            if line[0] == '-':
                out.append(0 - int(line[1:]))
            else:
                out.append(int(line[1:]))
    return out


def process_data_part_1(data):
    return sum(data)


def process_data_part_2(data):
    frequencies = set()
    cur_freq = 0
    calibrated = False
    while not calibrated:
        for change in data:
            cur_freq += change
            if cur_freq in frequencies:
                calibrated = True
                break
            frequencies.add(cur_freq)
    return cur_freq

if __name__ == "__main__":
    data = read_input()
    print(process_data_part_1(data))
    print(process_data_part_2(data))