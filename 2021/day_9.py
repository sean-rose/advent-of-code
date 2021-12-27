#!/usr/bin/env python

from pathlib import Path
from typing import Optional


FILE_PATH = Path(__file__)


class Point:
    def __init__(self, x: int, y: int, height: int) -> None:
        self.x = x
        self.y = y
        self.height = height
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


def find_low_points(heightmap: list[list[Point]]) -> list[Point]:
    low_points = []
    for row in heightmap:
        for point in row:
            if (
                (point.y == 0 or point.height < heightmap[point.y - 1][point.x].height)
                and (point.y == (len(heightmap) - 1) or point.height < heightmap[point.y + 1][point.x].height)
                and (point.x == 0 or point.height < heightmap[point.y][point.x - 1].height)
                and (point.x == (len(heightmap[point.y]) - 1) or point.height < heightmap[point.y][point.x + 1].height)
            ):
                low_points.append(point)
    return low_points


def find_basin_points(heightmap: list[list[Point]], low_point: Point, found_basin_points: Optional[set[Point]] = None) -> set[Point]:
    basin_points: set[Point] = set()
    if found_basin_points:
        basin_points.update(found_basin_points)
    basin_points.add(low_point)

    adjascent_points: list[Point] = []
    if low_point.y > 0:
        adjascent_points.append(heightmap[low_point.y - 1][low_point.x])
    if low_point.y < (len(heightmap) - 1):
        adjascent_points.append(heightmap[low_point.y + 1][low_point.x])
    if low_point.x > 0:
        adjascent_points.append(heightmap[low_point.y][low_point.x - 1])
    if low_point.x < (len(heightmap[low_point.y]) - 1):
        adjascent_points.append(heightmap[low_point.y][low_point.x + 1])

    for adjascent_point in adjascent_points:
        if (
            adjascent_point.height >= low_point.height
            and adjascent_point.height < 9
            and adjascent_point not in basin_points
        ):
            basin_points.update(find_basin_points(heightmap, adjascent_point, basin_points))

    return basin_points


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        heightmap = [
            [Point(x, y, int(height_str)) for x, height_str in enumerate(line.rstrip())]
            for y, line in enumerate(file)
        ]

    low_points = find_low_points(heightmap)
    risk_levels = [point.height + 1 for point in low_points]
    risk_levels_sum = sum(risk_levels)
    print(f"Sum of the risk levels of all low points:  {risk_levels_sum}")

    basins = [find_basin_points(heightmap, low_point) for low_point in low_points]
    basins.sort(key=lambda basin: len(basin), reverse=True)
    largest_basins_product = len(basins[0]) * len(basins[1]) * len(basins[2])
    print(f"Product of sizes of the three largest basins:  {largest_basins_product}")
