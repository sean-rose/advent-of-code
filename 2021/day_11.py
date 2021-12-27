#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


class Octopus():
    def __init__(self, x: int, y: int, energy_level: int) -> None:
        self.x = x
        self.y = y
        self.energy_level = energy_level
        self.has_just_flashed = False

    def __repr__(self) -> str:
        return str(self.energy_level)


def increase_octopus_energy_level(octopus: Octopus, octopus_grid: list[list[Octopus]]) -> None:
    if octopus.has_just_flashed:
        return

    octopus.energy_level += 1

    if octopus.energy_level > 9:
        octopus.energy_level = 0
        octopus.has_just_flashed = True

        adjascent_diffs = (
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        )
        for diff_x, diff_y in adjascent_diffs:
            adjascent_x = octopus.x + diff_x
            adjascent_y = octopus.y + diff_y
            if 0 <= adjascent_x < len(octopus_grid[octopus.y]) and 0 <= adjascent_y < len(octopus_grid):
                increase_octopus_energy_level(octopus_grid[adjascent_y][adjascent_x], octopus_grid)


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        octopus_grid = [
            [Octopus(x, y, int(energy_level_str)) for x, energy_level_str in enumerate(line.rstrip())]
            for y, line in enumerate(file)
        ]

    octopi = [octopus for row in octopus_grid for octopus in row]
    total_flash_count = 0
    for step in range(1, 101):
        step_flash_count = 0
        for octopus in octopi:
            increase_octopus_energy_level(octopus, octopus_grid)
        for octopus in octopi:
            if octopus.has_just_flashed:
                step_flash_count += 1
                octopus.has_just_flashed = False
        print(f"Step {step} flashes:  {step_flash_count}")
        total_flash_count += step_flash_count
    print(f"Total flashes after {step} steps:  {total_flash_count}")
