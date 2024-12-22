from typing import List, Tuple, Dict, Optional
import re
import heapq

# Type aliases
Position = Tuple[int, int]
Path = str
Cost = int
QueueState = List[int | Position | str]

# Constants
KEYPAD_MAIN: List[str] = ["789", "456", "123", " 0A"]
KEYPAD_NAVIGATION: List[str] = [" ^A", "<v>"]
MOVES = ["^", "<", "v", ">", "A"]
START_POSITIONS = {
    "^": (0, 1),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "A": (0, 2)
}
MOVE_CACHE: Dict[Tuple[str, str, int], int] = {}


def read_input(file_path: str = "input_sample") -> str:
    with open(file_path, "r") as file:
        return file.read().strip()


def get_keypad_value(position: Position, pad: List[str]) -> Optional[str]:
    row, column = position
    if not (0 <= row < len(pad) and 0 <= column < len(pad[row])):
        return None
    if pad[row][column] == " ":
        return None
    return pad[row][column]


def apply_move(position: Position, direction: str, pad: List[str]) -> Tuple[Position, Optional[str]]:
    moves = {
        "A": lambda pos: (pos, get_keypad_value(pos, pad)),
        "<": lambda pos: ((pos[0], pos[1] - 1), None),
        "^": lambda pos: ((pos[0] - 1, pos[1]), None),
        ">": lambda pos: ((pos[0], pos[1] + 1), None),
        "v": lambda pos: ((pos[0] + 1, pos[1]), None),
    }
    return moves[direction](position)


def find_shortest_path(target_code: str, pad_depth: int) -> int:
    initial_state: QueueState = [0, (3, 2), "A", "", ""]
    queue: List[QueueState] = []
    visited: Dict[Tuple[Position, str, str], int] = {}
    heapq.heappush(queue, initial_state)

    while queue:
        distance, current_position, current_direction, current_output, path = heapq.heappop(queue)
        if current_output == target_code:
            return distance
        if not target_code.startswith(current_output):
            continue
        if get_keypad_value(current_position, KEYPAD_MAIN) is None:
            continue

        state_key = (current_position, current_direction, current_output)
        if state_key in visited:
            continue
        visited[state_key] = distance

        for move in MOVES:
            new_position, output = apply_move(current_position, move, KEYPAD_MAIN)
            new_output = current_output + output if output is not None else current_output
            move_cost = calculate_move_cost(move, current_direction, pad_depth)
            heapq.heappush(queue, [distance + move_cost, new_position, move, new_output, path])


def calculate_move_cost(destination: str, current_move: str, pad_depth: int) -> int:
    cache_key = (destination, current_move, pad_depth)
    if cache_key in MOVE_CACHE:
        return MOVE_CACHE[cache_key]
    if pad_depth == 0:
        return 1

    search_queue: List[QueueState] = []
    initial_position = START_POSITIONS[current_move]
    visited_states: Dict[Tuple[Position, str], int] = {}
    heapq.heappush(search_queue, [0, initial_position, "A", "", ""])

    while search_queue:
        cost, position, current_direction, output, path = heapq.heappop(search_queue)
        if get_keypad_value(position, KEYPAD_NAVIGATION) is None:
            continue
        if output == destination:
            MOVE_CACHE[cache_key] = cost
            return cost
        elif len(output) > 0:
            continue

        state_key = (position, current_direction)
        if state_key in visited_states:
            continue
        visited_states[state_key] = cost

        for next_move in MOVES:
            next_position, next_output = apply_move(position, next_move, KEYPAD_NAVIGATION)
            next_cost = calculate_move_cost(next_move, current_direction, pad_depth - 1)
            new_output = output + next_output if next_output is not None else output
            heapq.heappush(search_queue, [
                cost + next_cost,
                next_position,
                next_move,
                new_output,
                path
            ])

if __name__ == "__main__":
    p1 = p2 = 0
    data = read_input("input")
    for line in data.split("\n"):
        s1 = find_shortest_path(line, 2)
        s2 = find_shortest_path(line, 25)
        line_int = [int(x) for x in re.findall("-?\d+", line)][0]
        p1 += line_int * s1
        p2 += line_int * s2

    print(p1)
    print(p2)
