from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue, PriorityQueue
from typing import TypeVar


class State(ABC):
    T = TypeVar('T', bound='State')

    def __init__(self, cost: int = 0):
        self.cost = cost

    @property
    @abstractmethod
    def is_finished(self) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def next_states(self) -> list[State.T]:
        raise NotImplemented

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplemented

    def __eq__(self, other: State.T) -> bool:
        return hash(self) == hash(other)

    def __lt__(self, other: State.T) -> bool:
        return self.cost < other.cost


def print_path(path: list[State.T]) -> None:
    print()
    print('Path:')
    print()
    for i, state in enumerate(path):
        if i:
            print(f'Step {i}, cost so far: {state.cost}')
            print()
        print(state)
        print()


def shortest_path(initial_state: State.T) -> list[State.T]:
    visited: set[State.T] = set()
    lowest_costs: dict[State.T, int] = {}
    prev_states: dict[State.T, State.T | None] = {initial_state: None}

    queue: Queue[State.T] = PriorityQueue()
    queue.put(initial_state)
    while state := queue.get():
        # state with lowest cost from the start so far
        if state.is_finished:
            # party time, get the complete path by traversing back to the start
            path = [state]
            while state := prev_states[state]:
                path.append(state)
            return list(reversed(path))

        # update costs for next possible states
        for next_state in state.next_states:
            if next_state in visited:
                # been there, done that
                continue

            if old_cost := lowest_costs.get(next_state):
                if next_state.cost >= old_cost:
                    # you can do better than that
                    continue

            # most efficient route to this state so far: update cost and add to queue
            lowest_costs[next_state] = next_state.cost
            queue.put(next_state)
            prev_states[next_state] = state

        visited.add(state)
