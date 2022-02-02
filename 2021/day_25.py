#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


def move_east(sea_cucumbers: tuple[str]) -> tuple[str]:
    return tuple(
        ''.join(
            '>' if char == '.' and line[x - 1] == '>'
            else '.' if char == '>' and line[(x + 1) % len(line)] == '.'
            else char
            for x, char in enumerate(line)
        )
        for line in sea_cucumbers
    )


def move_south(sea_cucumbers: tuple[str]) -> tuple[str]:
    return tuple(
        ''.join(
            'v' if char == '.' and sea_cucumbers[y - 1][x] == 'v'
            else '.' if char == 'v' and sea_cucumbers[(y + 1) % len(sea_cucumbers)][x] == '.'
            else char
            for x, char in enumerate(line)
        )
        for y, line in enumerate(sea_cucumbers)
    )


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        sea_cucumbers = tuple(line.rstrip() for line in file if line.rstrip())

    step = 0
    previous_sea_cucumbers = None
    while sea_cucumbers != previous_sea_cucumbers:
        step += 1
        previous_sea_cucumbers = sea_cucumbers
        sea_cucumbers = move_east(sea_cucumbers)
        sea_cucumbers = move_south(sea_cucumbers)
    print('\n'.join(sea_cucumbers))
    print(f"Sea cucumbers stopped moving after step {step}.")
