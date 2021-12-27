#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


class Cave():
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_start = name == 'start'
        self.is_end = name == 'end'
        self.is_large = name == name.upper()
        self.adjascent_caves: list[Cave] = []

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name


def find_paths_not_repeating_small_caves(start_path: list[Cave]) -> list[list[Cave]]:
    paths: list[list[Cave]] = []
    for adjascent_cave in start_path[-1].adjascent_caves:
        extended_path = start_path + [adjascent_cave]
        if adjascent_cave.is_end:
            paths.append(extended_path)
        elif adjascent_cave.is_large or adjascent_cave not in start_path:
            paths.extend(find_paths_not_repeating_small_caves(extended_path))
    return paths


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        cave_connections = [line.rstrip().split('-') for line in file]

    caves: dict[str, Cave] = {}
    for cave_1_name, cave_2_name in cave_connections:
        if cave_1_name not in caves:
            caves[cave_1_name] = Cave(cave_1_name)
        cave_1 = caves[cave_1_name]

        if cave_2_name not in caves:
            caves[cave_2_name] = Cave(cave_2_name)
        cave_2 = caves[cave_2_name]

        cave_1.adjascent_caves.append(cave_2)
        cave_2.adjascent_caves.append(cave_1)

    paths = find_paths_not_repeating_small_caves([caves['start']])
    print(f"Found {len(paths)} paths that don't repeat small caves:")
    for path in paths:
        print(','.join(str(cave) for cave in path))
