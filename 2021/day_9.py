#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


def find_low_points(heightmap: list[list[int]]) -> list[int]:
    low_points = []
    for row, heights in enumerate(heightmap):
        for column, height in enumerate(heights):
            if (
                (row == 0 or height < heightmap[row - 1][column])
                and (row == (len(heightmap) - 1) or height < heightmap[row + 1][column])
                and (column == 0 or height < heightmap[row][column - 1])
                and (column == (len(heightmap[row]) - 1) or height < heightmap[row][column + 1])
            ):
                low_points.append(height)
    return low_points


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        heightmap = [[int(number_str) for number_str in line.rstrip()] for line in file]

    low_points = find_low_points(heightmap)
    risk_levels = [height + 1 for height in low_points]
    risk_levels_sum = sum(risk_levels)
    print(f"Sum of the risk levels of all low points:  {risk_levels_sum}")
