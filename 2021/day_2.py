#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


def move_submarine(commands: list[str]) -> tuple[int, int]:
    horizontal_position = 0
    depth = 0

    for command in commands:
        move, distance = command.split()
        if move == 'forward':
            horizontal_position += int(distance)
        elif move == 'down':
            depth += int(distance)
        elif move == 'up':
            depth -= int(distance)
        else:
            raise Exception(f"Unknown command:  {command}")

    return horizontal_position, depth


def move_submarine_2(commands: list[str]) -> tuple[int, int]:
    aim = 0
    horizontal_position = 0
    depth = 0

    for command in commands:
        move, amount = command.split()
        if move == 'forward':
            horizontal_position += int(amount)
            depth += aim * int(amount)
        elif move == 'down':
            aim += int(amount)
        elif move == 'up':
            aim -= int(amount)
        else:
            raise Exception(f"Unknown command:  {command}")

    return horizontal_position, depth


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        commands = file.readlines()

    print("--- Part One ---")
    horizontal_position, depth = move_submarine(commands)
    multiplied = horizontal_position * depth
    print(f"Horizontal position:  {horizontal_position}")
    print(f"Depth:  {depth}")
    print(f"Multiplied:  {multiplied}")

    print("--- Part Two ---")
    horizontal_position, depth = move_submarine_2(commands)
    multiplied = horizontal_position * depth
    print(f"Horizontal position:  {horizontal_position}")
    print(f"Depth:  {depth}")
    print(f"Multiplied:  {multiplied}")
