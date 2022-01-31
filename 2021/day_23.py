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

ORGANIZED_FOLDED_MAP = (
    '#############',
    '#...........#',
    '###A#B#C#D###',
    '  #A#B#C#D#',
    '  #########'
)

ORGANIZED_UNFOLDED_MAP = (
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

Map = Tuple[str, ...]

Space = Tuple[int, int]


class Move:
    def __init__(self, map: Map, energy_used: int = 0, previous_move: Optional[Move] = None) -> None:
        self.map = map
        self.energy_used = energy_used
        self.total_energy_used = previous_move.total_energy_used + energy_used if previous_move else energy_used
        self.previous_move = previous_move


def try_get_room(space: Space, room_spaces: dict[str, list[Space]]) -> Optional[str]:
    for room, spaces in room_spaces.items():
        if space in spaces:
            return room
    return None


def get_adjascent_spaces(map: Map, space: Space) -> list[Space]:
    return [
        (new_x, new_y)
        for new_x, new_y in (
            (space[0] + diff_x, space[1] + diff_y)
            for diff_x, diff_y in ADJASCENT_DIFFS
        )
        if 0 <= new_y < len(map)
            and 0 <= new_x < len(map[new_y])
            and map[new_y][new_x] == '.'
    ]


def find_reachable_spaces_steps(map: Map, from_space: Space, exclude_space: Optional[Space] = None, steps: int = 0) -> list[tuple[Space, int]]:
    adjascent_spaces_steps = [(space, steps + 1) for space in get_adjascent_spaces(map, from_space) if space != exclude_space]
    reachable_spaces_steps = adjascent_spaces_steps.copy()
    for adjascent_space, adjascent_steps in adjascent_spaces_steps:
        reachable_spaces_steps.extend(find_reachable_spaces_steps(map, adjascent_space, from_space, adjascent_steps))
    return reachable_spaces_steps


def find_amphipod_moves(current_move: Move, room_spaces: dict[str, list[Space]]) -> list[Move]:
    moves: list[Move] = []
    for y, line in enumerate(current_move.map):
        for x, char in enumerate(line):
            if char in ('A', 'B', 'C', 'D'):
                amphipod_type = char
                from_space = (x, y)
                from_room = try_get_room(from_space, room_spaces)
                if from_room and amphipod_type == from_room:
                    from_room_spaces = room_spaces[from_room]
                    from_room_space_index = from_room_spaces.index(from_space)
                    if not any(
                        current_move.map[from_room_space[1]][from_room_space[0]] != amphipod_type
                        for from_room_space in from_room_spaces[from_room_space_index + 1:]
                    ):
                        continue
                for to_space, steps in find_reachable_spaces_steps(current_move.map, from_space):
                    to_room = try_get_room(to_space, room_spaces)
                    if to_room:
                        to_room_spaces = room_spaces[to_room]
                        to_room_space_index = to_room_spaces.index(to_space)
                        if (
                            to_room != amphipod_type
                            or any(
                                current_move.map[to_room_space[1]][to_room_space[0]] not in (amphipod_type, '.')
                                for to_room_space in to_room_spaces
                            )
                            or any(
                                current_move.map[to_room_space[1]][to_room_space[0]] == '.'
                                for to_room_space in to_room_spaces[to_room_space_index + 1:]
                            )
                        ):
                            continue
                    elif from_room is None:
                        continue
                    elif try_get_room((to_space[0], to_space[1] + 1), room_spaces) is not None:
                        continue
                    new_map = move_amphipod(current_move.map, from_space, to_space)
                    moves.append(Move(new_map, steps * STEP_ENERGY[amphipod_type], current_move))
    return moves


def move_amphipod(map: Map, from_space: Space, to_space: Space) -> Map:
    amphipod_type = map[from_space[1]][from_space[0]]
    return tuple(
        line if y not in (from_space[1], to_space[1])
        else ''.join(
                amphipod_type if x == to_space[0] and y == to_space[1]
                else '.' if x == from_space[0] and y == from_space[1]
                else char
                for x, char in enumerate(line)
            )
        for y, line in enumerate(map)
    )


def organize_amphipods(map: Map, organized_map: Map) -> list[Move]:
    start_move = Move(map)
    least_energy_moves_to_state: dict[Map, Move] = {
        map: start_move
    }

    room_spaces: dict[str, list[Space]] = defaultdict(list)
    for y, line in enumerate(organized_map):
        for x, char in enumerate(line):
            if char in ('A', 'B', 'C', 'D'):
                room_spaces[char].append((x, y))

    moves_to_explore: dict[Map, Move] = {
        move.map: move
        for move in find_amphipod_moves(start_move, room_spaces)
    }
    explored_move_count = 0
    ignored_local_suboptimal_move_count = 0
    ignored_global_suboptimal_move_count = 0

    while moves_to_explore:
        new_map, move = moves_to_explore.popitem()

        if new_map in least_energy_moves_to_state and move.total_energy_used >= least_energy_moves_to_state[new_map].total_energy_used:
            ignored_local_suboptimal_move_count += 1
            continue

        if organized_map in least_energy_moves_to_state and move.total_energy_used >= least_energy_moves_to_state[organized_map].total_energy_used:
            ignored_global_suboptimal_move_count += 1
            continue

        least_energy_moves_to_state[new_map] = move
        if new_map == organized_map:
            print(f"Found solution that uses {move.total_energy_used} energy.")

        for next_move in find_amphipod_moves(move, room_spaces):
            if next_move.map in moves_to_explore and next_move.total_energy_used >= moves_to_explore[next_move.map].total_energy_used:
                ignored_local_suboptimal_move_count += 1
                continue
            moves_to_explore[next_move.map] = next_move

        explored_move_count += 1
        if explored_move_count % 100000 == 0:
            print(f"Explored {explored_move_count} moves.")

    print(f"Explored {explored_move_count} moves.")
    print(f"Ignored {ignored_local_suboptimal_move_count} locally suboptimal moves.")
    print(f"Ignored {ignored_global_suboptimal_move_count} globally suboptimal moves.")

    move_traceback = []
    move = least_energy_moves_to_state[organized_map]
    while move:
        move_traceback.append(move)
        move = move.previous_move
    return list(reversed(move_traceback))


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        folded_map = tuple(line.rstrip() for line in file if line.rstrip())
        print("Folded map:")
        print("\n".join(folded_map))

    folded_map_moves = organize_amphipods(folded_map, ORGANIZED_FOLDED_MAP)
    print(f"Least energy solution for folded map has {len(folded_map_moves)} moves.")
    for move in folded_map_moves:
        print("\n".join(move.map))
        print(f"Energy used:  {move.energy_used}")
    print(f"Total energy used for folded map:  {folded_map_moves[-1].total_energy_used}")

    unfolded_map = (
        folded_map[:3]
        + (
            '  #D#C#B#A#',
            '  #D#B#A#C#'
        )
        + folded_map[3:]
    )
    print("Unfolded map:")
    print("\n".join(unfolded_map))

    unfolded_map_moves = organize_amphipods(unfolded_map, ORGANIZED_UNFOLDED_MAP)
    print(f"Least energy solution for unfolded map has {len(unfolded_map_moves)} moves.")
    for move in unfolded_map_moves:
        print("\n".join(move.map))
        print(f"Energy used:  {move.energy_used}")
    print(f"Total energy used for unfolded map:  {unfolded_map_moves[-1].total_energy_used}")
