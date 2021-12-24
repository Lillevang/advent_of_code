from typing import List, Tuple, Dict
import sys

def read_input() -> List[int]:
    with open('./input', 'r') as file:
        return [int(line.split(": ")[1]) for line in file.readlines()]


class DiracDice:

    def __init__(self, starting_positions : List[int]) -> None:
        self.p1 = Player(starting_positions[0], 'p1')
        self.p2 = Player(starting_positions[1], 'p2')
        self.p1.other_player = self.p2
        self.p2.other_player = self.p1
        self.no_of_rolls = 0
        self.last_roll = 0
        self.player_turn = self.p1


    def play(self):
        while self.p1.points < 1000 and self.p2.points < 1000:
            sum_of_rolls = self.roll_deterministic_dice()
            cur_pos = self.player_turn.position
            self.player_turn.move(sum_of_rolls)
            print(f'{self.player_turn._id} moved {sum_of_rolls} from {cur_pos} to {self.player_turn.position}. Points now: {self.player_turn.points}')
            if not self.player_turn.points >= 1000:
                self.player_turn = self.player_turn.other_player
        print(f'Game finished. {self.player_turn._id} won with {self.player_turn.points} points.')


    def roll_deterministic_dice(self) -> int:
        sum_of_rolls = self.last_roll + 1 + self.last_roll + 2 + self.last_roll + 3
        self.last_roll = self.last_roll + 3
        self.no_of_rolls += 3
        return sum_of_rolls


class Player:

    def __init__(self, starting_position : int, _id : str) -> None:
        self._id = _id
        self.position = starting_position
        self.points = 0
        self.other_player = None

    def move(self, sum_of_rolls : int) -> None:
        self.position = (self.position + (sum_of_rolls % 10)) % 10
        if self.position == 0:
            self.position = 10
        self.points += self.position

def part_one(starting_positions : List[int]) -> int:
    game = DiracDice(starting_positions)
    game.play()
    print(f'{game.player_turn.other_player.points} * {game.no_of_rolls}')
    return game.player_turn.other_player.points * game.no_of_rolls

def count_win(player_1_pos : int, player_2_pos : int, player_1_score : int, player_2_score : int, game_state : Dict[Tuple[int, int, int, int], Tuple[int, int]]):
  # Given that A is at position p1 with score s1, and B is at position p2 with score s2, and A is to move,
  # return (# of universes where player A wins, # of universes where player B wins)
    if player_1_score >= 21:
        return (1,0)
    elif player_2_score >= 21:
        return (0, 1)
    elif (player_1_pos, player_2_pos, player_1_score, player_2_score) in game_state:
        return game_state[(player_1_pos, player_2_pos, player_1_score, player_2_score)]
    ans = (0,0) # Holds number of wins for each player
    for d1 in [1,2,3]:
        for d2 in [1,2,3]:
            for d3 in [1,2,3]:
                new_player_1_pos = (player_1_pos+d1+d2+d3)%10
                new_player_1_score = player_1_score + new_player_1_pos + 1
                x1, y1 = count_win(player_2_pos, new_player_1_pos, player_2_score, new_player_1_score, game_state)
                ans = (ans[0]+y1, ans[1]+x1)
    game_state[(player_1_pos, player_2_pos, player_1_score, player_2_score)] = ans
    return ans


def part_two():
    # OOP approach for p1 is not feasible for the second part as we have to create three new games everytime the dice is rolled.
    # Instead approach will be a recursive solution
    player_1_pos = 4-1
    player_2_pos = 2-1
    game_state = {}
    return max(count_win(player_1_pos, player_2_pos, 0, 0, game_state))

def main() -> None:
    starting_positions = read_input()
    try:
        if sys.argv[1] == '1':
            print(part_one(starting_positions))
        elif sys.argv[1] == '2':
            print(part_two())
    except:
        print(part_one(starting_positions))
        print(part_two(starting_positions))


if __name__ == '__main__':
    main()
