from typing import List
import copy

def read_input(path='input') -> List[int]:
    with open(path, 'r') as file:
        return [int(_.strip()) for _ in file.readline().split(',')]


def process_opcodes(data, noun=12, verb=2) -> int:
    data[1] = noun
    data[2] = verb
    for i in range(0, len(data), 4):
        if data[i] == 1:
            data[data[i+3]] = data[data[i + 1]] + data[data[i + 2]]
        elif data[i] == 2:
            data[data[i+3]] = data[data[i + 1]] * data[data[i + 2]]
        elif data[i] == 99:
            break
    return data[0]


def find_noun_and_verb(data: List[int]) -> int:
    for i in range(100):
        for j in range(100):
            if process_opcodes(copy.deepcopy(data), i, j) == 19690720:
                return 100 * i + j
    return None


if __name__ == "__main__":
    data = read_input()
    print(process_opcodes(copy.deepcopy(data)))
    print(find_noun_and_verb(data))
    
