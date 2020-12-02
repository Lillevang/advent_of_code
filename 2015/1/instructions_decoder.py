
def read_input(path='input') -> str:
    with open(path, 'r') as file:
        return file.readline()


def process_instruction_part_1(_instruction: str) -> int:
    up_moves = _instruction.count('(')
    down_moves = _instruction.count(')')
    return up_moves - down_moves


def process_instruction_part_2(_instruction: str) -> int:
    current_floor = 0       
    for idx, _ in enumerate(_instruction):
        if _ == '(':
            current_floor += 1
        elif _ == ')':
            current_floor -= 1
        if current_floor < 0:
            return idx + 1
       

if __name__ == "__main__":
    _instruction = read_input()
    print(process_instruction_part_1(_instruction))
    print(process_instruction_part_2(_instruction))