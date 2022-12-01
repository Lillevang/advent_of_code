from __future__ import annotations

from copy import copy
from dataclasses import dataclass

import dijkstra


@dataclass
class Room:
    _amphipod_type: int
    _size: int
    _content: list[int]

    def __repr__(self) -> str:
        return f'{self._content}'

    def __copy__(self) -> Room:
        return Room(self._amphipod_type, self._size, self._content[:])

    @property
    def first(self) -> int:
        return self._content[-1]

    def get(self, i: int) -> int:
        try:
            return self._content[i]
        except IndexError:
            return 0

    @property
    def is_clean(self) -> bool:
        return all(amphipod == self._amphipod_type for amphipod in self._content)

    @property
    def is_empty(self) -> bool:
        return not self._content

    @property
    def is_full(self) -> bool:
        return len(self._content) == self._size

    @property
    def spots_left(self) -> int:
        return self._size - len(self._content)

    def can_add(self, amphipod: int) -> bool:
        return amphipod == self._amphipod_type and not self.is_full and self.is_clean

    def add(self, amphipod: int) -> None:
        self._content.append(amphipod)

    def remove(self) -> int:
        return self._content.pop()


class AmphipodState(dijkstra.State):
    def __init__(
        self,
        room_size: int,
        rooms: list[Room],
        hallway: list[int] = None,
        cost: int = 0,
    ):
        super().__init__(cost)
        self._room_size = room_size
        self._rooms = rooms
        self._hallway = hallway or [0] * 7

    @classmethod
    def from_input(cls, input_lines: list[str]) -> AmphipodState:
        room_size = len(input_lines)
        return AmphipodState(room_size, rooms=[
            Room(name, room_size, [{'A': 1, 'B': 2, 'C': 3, 'D': 4}[c] for c in content])
            for name, content in zip(
                [1, 2, 3, 4],
                list(zip(*[line[3:10:2] for line in input_lines])),
            )
        ])

    def __hash__(self) -> int:
        return hash(f'{self._rooms}{self._hallway}')

    @property
    def is_finished(self) -> bool:
        return self.cost and not sum(self._hallway)

    def _can_move(self, room: int, hall: int) -> bool:
        # Trust me, I'm an engineer
        return not (
            hall < room + 1 and any(self._hallway[hall + 1:room + 2]) or
            hall > room + 2 and any(self._hallway[room + 2:hall])
        )

    def move(self, amphipod: int, r: int, h: int, into_room: bool) -> AmphipodState:
        rooms = [copy(room) for room in self._rooms]
        hallway = self._hallway[:]
        if into_room:
            rooms[r].add(hallway[h])
            hallway[h] = 0
        else:
            hallway[h] = rooms[r].remove()
        # Trust me, I'm an engineer
        steps = abs(h * 2 - r * 2 - 3) + 1 - int(h in (0, 6)) + rooms[r].spots_left - int(into_room)
        return AmphipodState(self._room_size, rooms, hallway, self.cost + steps * 10 ** (amphipod - 1))

    @property
    def next_states(self) -> list[AmphipodState]:
        return [
            # all states that move an amphipod out of a room
            self.move(room.first, r, h, into_room=False)
            for r, room in enumerate(self._rooms) if not room.is_clean and not room.is_empty
            for h, amphipod in enumerate(self._hallway) if not amphipod and self._can_move(r, h)
        ] + [
            # all states that move an amphipod into a room
            self.move(amphipod, r, h, into_room=True)
            for h, amphipod in enumerate(self._hallway) if amphipod
            for r, room in enumerate(self._rooms) if room.can_add(amphipod) and self._can_move(r, h)
        ]

    def __repr__(self) -> str:
        """
        Code is not meant to look readable, just to print the mushroom.

        #############
        #CA...B.C.BB#
        ###.#.#.#D###
          #D#.#.#A#
          #D#B#.#C#
          #A#D#C#A#
          #########
        """
        def p(i): 
            return '  ' if i else '##'
        s = '.ABCD'
        h = '.'.join(s[a] for a in self._hallway)
        rs = self._room_size
        return (
            '#' * 13 + '\n#' + h[0] + h[2:-2] + h[-1] + '#\n' + '\n'.join(p(i) + '#' + '#'.join(
                s[r.get(rs - i - 1)] for r in self._rooms
            ) + '#' + p(i) for i in range(rs)) + '\n  ' + '#' * 9 + '  '
        )


def part1(input_lines: list[str]) -> int:
    path = dijkstra.shortest_path(AmphipodState.from_input(input_lines[5:1:-3]))
    dijkstra.print_path(path)
    return path[-1].cost


def part2(input_lines: list[str]) -> int:
    path = dijkstra.shortest_path(AmphipodState.from_input(input_lines[5:1:-1]))
    dijkstra.print_path(path)
    return path[-1].cost

input_lines = open('./input.txt').read().splitlines()
print(part2(input_lines))
