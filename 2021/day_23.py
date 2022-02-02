#!/usr/bin/env python

from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from typing import Optional, Tuple


FILE_PATH = Path(__file__)

STEP_ENERGY = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

ORGANIZED_FOLDED_DIAGRAM = (
    '#############',
    '#...........#',
    '###A#B#C#D###',
    '  #A#B#C#D#',
    '  #########'
)

ORGANIZED_UNFOLDED_DIAGRAM = (
    '#############',
    '#...........#',
    '###A#B#C#D###',
    '  #A#B#C#D#',
    '  #A#B#C#D#',
    '  #A#B#C#D#',
    '  #########'
)

ADJASCENT_DIFFS = (
              (0, -1),
    (-1,  0),          (1,  0),
              (0,  1)
)

Diagram = Tuple[str, ...]

Space = Tuple[int, int]


class Move:
    def __init__(self, diagram: Diagram, energy_used: int = 0, previous_move: Optional[Move] = None) -> None:
        self.diagram = diagram
        self.energy_used = energy_used
        self.total_energy_used = previous_move.total_energy_used + energy_used if previous_move else energy_used
        self.previous_move = previous_move


def try_get_room(space: Space, room_spaces: dict[str, list[Space]]) -> Optional[str]:
    for room, spaces in room_spaces.items():
        if space in spaces:
            return room
    return None


def get_adjascent_spaces(diagram: Diagram, space: Space) -> list[Space]:
    return [
        (new_x, new_y)
        for new_x, new_y in (
            (space[0] + diff_x, space[1] + diff_y)
            for diff_x, diff_y in ADJASCENT_DIFFS
        )
        if 0 <= new_y < len(diagram)
            and 0 <= new_x < len(diagram[new_y])
            and diagram[new_y][new_x] == '.'
    ]


def find_reachable_spaces_steps(diagram: Diagram, from_space: Space, exclude_space: Optional[Space] = None, steps: int = 0) -> list[tuple[Space, int]]:
    adjascent_spaces_steps = [(space, steps + 1) for space in get_adjascent_spaces(diagram, from_space) if space != exclude_space]
    reachable_spaces_steps = adjascent_spaces_steps.copy()
    for adjascent_space, adjascent_steps in adjascent_spaces_steps:
        reachable_spaces_steps.extend(find_reachable_spaces_steps(diagram, adjascent_space, from_space, adjascent_steps))
    return reachable_spaces_steps


def find_amphipod_moves(current_move: Move, room_spaces: dict[str, list[Space]]) -> list[Move]:
    moves: list[Move] = []
    for y, line in enumerate(current_move.diagram):
        for x, char in enumerate(line):
            if char in ('A', 'B', 'C', 'D'):
                amphipod_type = char
                from_space = (x, y)
                from_room = try_get_room(from_space, room_spaces)
                if from_room and amphipod_type == from_room:
                    from_room_spaces = room_spaces[from_room]
                    from_room_space_index = from_room_spaces.index(from_space)
                    if not any(
                        current_move.diagram[from_room_space[1]][from_room_space[0]] != amphipod_type
                        for from_room_space in from_room_spaces[from_room_space_index + 1:]
                    ):
                        continue
                for to_space, steps in find_reachable_spaces_steps(current_move.diagram, from_space):
                    to_room = try_get_room(to_space, room_spaces)
                    if to_room:
                        to_room_spaces = room_spaces[to_room]
                        to_room_space_index = to_room_spaces.index(to_space)
                        if (
                            to_room != amphipod_type
                            or any(
                                current_move.diagram[to_room_space[1]][to_room_space[0]] not in (amphipod_type, '.')
                                for to_room_space in to_room_spaces
                            )
                            or any(
                                current_move.diagram[to_room_space[1]][to_room_space[0]] == '.'
                                for to_room_space in to_room_spaces[to_room_space_index + 1:]
                            )
                        ):
                            continue
                    elif from_room is None:
                        continue
                    elif try_get_room((to_space[0], to_space[1] + 1), room_spaces) is not None:
                        continue
                    new_diagram = move_amphipod(current_move.diagram, from_space, to_space)
                    moves.append(Move(new_diagram, steps * STEP_ENERGY[amphipod_type], current_move))
    return moves


def move_amphipod(diagram: Diagram, from_space: Space, to_space: Space) -> Diagram:
    amphipod_type = diagram[from_space[1]][from_space[0]]
    return tuple(
        line if y not in (from_space[1], to_space[1])
        else ''.join(
                amphipod_type if x == to_space[0] and y == to_space[1]
                else '.' if x == from_space[0] and y == from_space[1]
                else char
                for x, char in enumerate(line)
            )
        for y, line in enumerate(diagram)
    )


def organize_amphipods(diagram: Diagram, organized_diagram: Diagram) -> list[Move]:
    start_move = Move(diagram)
    least_energy_moves_to_state: dict[Diagram, Move] = {
        diagram: start_move
    }

    room_spaces: dict[str, list[Space]] = defaultdict(list)
    for y, line in enumerate(organized_diagram):
        for x, char in enumerate(line):
            if char in ('A', 'B', 'C', 'D'):
                room_spaces[char].append((x, y))

    moves_to_explore: dict[Diagram, Move] = {
        move.diagram: move
        for move in find_amphipod_moves(start_move, room_spaces)
    }
    explored_move_count = 0
    ignored_local_suboptimal_move_count = 0
    ignored_global_suboptimal_move_count = 0

    while moves_to_explore:
        new_diagram, move = moves_to_explore.popitem()

        if new_diagram in least_energy_moves_to_state and move.total_energy_used >= least_energy_moves_to_state[new_diagram].total_energy_used:
            ignored_local_suboptimal_move_count += 1
            continue

        if organized_diagram in least_energy_moves_to_state and move.total_energy_used >= least_energy_moves_to_state[organized_diagram].total_energy_used:
            ignored_global_suboptimal_move_count += 1
            continue

        least_energy_moves_to_state[new_diagram] = move
        if new_diagram == organized_diagram:
            print(f"Found solution that uses {move.total_energy_used} energy.")

        for next_move in find_amphipod_moves(move, room_spaces):
            if next_move.diagram in moves_to_explore and next_move.total_energy_used >= moves_to_explore[next_move.diagram].total_energy_used:
                ignored_local_suboptimal_move_count += 1
                continue
            moves_to_explore[next_move.diagram] = next_move

        explored_move_count += 1
        if explored_move_count % 100000 == 0:
            print(f"Explored {explored_move_count} moves.")

    print(f"Explored {explored_move_count} moves.")
    print(f"Ignored {ignored_local_suboptimal_move_count} locally suboptimal moves.")
    print(f"Ignored {ignored_global_suboptimal_move_count} globally suboptimal moves.")

    move_traceback = []
    move = least_energy_moves_to_state[organized_diagram]
    while move:
        move_traceback.append(move)
        move = move.previous_move
    return list(reversed(move_traceback))


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        folded_diagram = tuple(line.rstrip() for line in file if line.rstrip())
        print("Folded diagram:")
        print("\n".join(folded_diagram))

    folded_diagram_moves = organize_amphipods(folded_diagram, ORGANIZED_FOLDED_DIAGRAM)
    print(f"Least energy solution for folded diagram has {len(folded_diagram_moves)} moves.")
    for move in folded_diagram_moves:
        print("\n".join(move.diagram))
        print(f"Energy used:  {move.energy_used}")
    print(f"Total energy used for folded diagram:  {folded_diagram_moves[-1].total_energy_used}")

    unfolded_diagram = (
        folded_diagram[:3]
        + (
            '  #D#C#B#A#',
            '  #D#B#A#C#'
        )
        + folded_diagram[3:]
    )
    print("Unfolded diagram:")
    print("\n".join(unfolded_diagram))

    unfolded_diagram_moves = organize_amphipods(unfolded_diagram, ORGANIZED_UNFOLDED_DIAGRAM)
    print(f"Least energy solution for unfolded diagram has {len(unfolded_diagram_moves)} moves.")
    for move in unfolded_diagram_moves:
        print("\n".join(move.diagram))
        print(f"Energy used:  {move.energy_used}")
    print(f"Total energy used for unfolded diagram:  {unfolded_diagram_moves[-1].total_energy_used}")
