from typing import List, Tuple
import re

PATTERN = re.compile(r'(?P<direction>\D{1})(?P<distance>\d+)')
DIRECTION = 'N'
DIRECTIONS = {
    'N': {
        'L': 'W',
        'R': 'E'},
    'E': {
        'L': 'N',
        'R': 'S'},
    'S': {
        'L': 'E',
        'R': 'W'},
    'W': {
        'L': 'S',
        'R': 'N'}}


def read_input(path='input') -> List:
    with open(path, 'r') as file:
        return [_.strip() for _ in file.readline().split(',')]


def parse_move_instruction(move: str) -> str and int:
    matches = PATTERN.search(move)
    _dir = matches.group('direction')
    _dist = int(matches.group('distance'))
    return _dir, _dist


def process_moves_part_1(moves: List) -> int:
    X = 0
    Y = 0
    for move in moves:
        _dir, _dist = parse_move_instruction(move)
        X, Y = change_position(_dir, _dist, X, Y)
    return abs(X) + abs(Y)


def process_moves_part_2(moves: List) -> int:
    X = 0
    Y = 0
    position_history = []
    for move in moves:
        _dir, _dist = parse_move_instruction(move)
        old_pos = (X, Y)
        X, Y = change_position(_dir, _dist, X, Y)
        new_pos = (X, Y)
        finished, _ = move_to_location(position_history, old_pos, new_pos)
        if finished:
            return abs(_[0]) + abs(_[1])


def move_to_location(position_history: List, old_pos, new_pos) -> bool and Tuple:
    global DIRECTION
    if DIRECTION == 'N' or DIRECTION == 'S':
        for i in range(old_pos[1], new_pos[1]):
            move = (old_pos[0], i)
            if move in position_history:
                return True, move
            position_history.append(move)
    else:
        for i in range(old_pos[0], new_pos[0]):
            move = (i, old_pos[1])
            if move in position_history:
                return True, move
            position_history.append(move)
    return False, new_pos


def change_position(_dir: str, _dist: int, X: int, Y: int):
    global DIRECTION
    DIRECTION = DIRECTIONS[DIRECTION][_dir]
    if DIRECTION == 'N':
        Y += _dist
    elif DIRECTION == 'E':
        X += _dist
    elif DIRECTION == 'S':
        Y -= _dist
    elif DIRECTION == 'W':
        X -= _dist
    else:
        print('Something went horribly wrong...')
    return X, Y


if __name__ == "__main__":
    moves = read_input()
    print(f'Part 1: {process_moves_part_1(moves)} moves to final location.')
    print(f'Part 2: {process_moves_part_2(moves)} moves to first location visited twice.')
