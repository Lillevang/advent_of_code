from typing import List

def read_input(path='input') -> List[int]:
    with open(path, 'r') as file:
        return [int(_.strip()) for _ in file.readline().split(',')]


def add(x: int, y: int) -> int:
    return x + y


def mult(x: int, y: int) -> int:
    return x * y


def process_opcodes(data):
    data[1] = 12
    data[2] = 2
    for i in range(0, len(data), 4):
        if data[i] == 1:
            data[data[i+3]] = add(data[data[i + 1]], data[data[i + 2]])
        elif data[i] == 2:
            data[data[i+3]] = mult(data[data[i + 1]], data[data[i + 2]])
        elif data[i] == 99:
            break
    return data[0]


if __name__ == "__main__":
    data = read_input()
    print(process_opcodes(data))
    
