from typing import List

VALID_NUMBERS_PART_1 = range(1,10)
VALID_NUMBERS_PART_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15]
NUM_LET_MAP = {10: 'A', 11: 'B', 12: 'C', 15: 'D'}

MODIFIER_PART_1 = {
    'U': -3,
    'D': 3,
    'R': 1,
    'L': -1}

MODIFIER_PART_2 = {
    1: {
        'D': 2
    },
    2: {
        'R': 1,
        'D': 4
    },
    3: {
        'U': -2,
        'R': 1,
        'L': -1,
        'D': 4
    },
    6: {
        'U': -4,
        'R': 1,
        'L': -1,
        'D': 4
    },
    7: {
        'U': -4,
        'R': 1,
        'L': -1,
        'D': 4
    },
    8: {
        'U': -4,
        'R': 1,
        'L': -1,
        'D': 4
    },
    11: {
        'U': -4,
        'R': 1,
        'L': -1,
        'D': 4
    },
    4: {
        'L': -1,
        'D': 4
    },
    5: {
        'R': 1
    },
    9: {
        'L': -1
    },
    10: {
        'R': 1,
        'U': -4
    },
    12: {
        'L': -1,
        'U': -4
    },
    15: {
        'U': -4
    }
}

def read_input(path='input'):
    with open(path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def move_is_valid_part_1(move: str, CURRENT_POSITION) -> bool:
    if CURRENT_POSITION == 1 and move not in ['L', 'U']:
        return True
    elif CURRENT_POSITION == 2 and move != 'U':
        return True
    elif CURRENT_POSITION == 3 and move not in ['R', 'U']:
        return True
    elif CURRENT_POSITION == 4 and move != 'L':
        return True
    elif CURRENT_POSITION == 5:
        return True
    elif CURRENT_POSITION == 6 and move != 'R':
        return True
    elif CURRENT_POSITION == 7 and move not in ['L', 'D']:
        return True
    elif CURRENT_POSITION == 8 and move != 'D':
        return True
    elif CURRENT_POSITION == 9 and move not in ['R', 'D']:
        return True
    else:
        return False


def move_part_2(move: str, CURRENT_POSITION) -> int:
    try:
        NEW_POSITION = CURRENT_POSITION + MODIFIER_PART_2[CURRENT_POSITION][move]
        if NEW_POSITION in VALID_NUMBERS_PART_2:
            return NEW_POSITION
        else:
            return CURRENT_POSITION
    except KeyError:
        return CURRENT_POSITION
       

def process_pattern_part_1(digits: List):
    CURRENT_POSITION = 5
    code = ''
    for digit in digits:
        for move in digit:
            if move_is_valid_part_1(move, CURRENT_POSITION):
                _mod = MODIFIER_PART_1[move]
                if CURRENT_POSITION + _mod in VALID_NUMBERS_PART_1:
                    CURRENT_POSITION += _mod
        code += str(CURRENT_POSITION)
    return code
            

def process_pattern_part_2(digits: List):
    CURRENT_POSITION = 5
    code = ''
    for digit in digits:
        for move in digit:
            CURRENT_POSITION = move_part_2(move, CURRENT_POSITION)
        if CURRENT_POSITION not in NUM_LET_MAP:
            code += str(CURRENT_POSITION)
        else:
            code += NUM_LET_MAP[CURRENT_POSITION]
    return code
        

if __name__ == "__main__":
    _lines = read_input()
    print(f'Part 1: {process_pattern_part_1(_lines)}')
    print(f'Part 2: {process_pattern_part_2(_lines)}')