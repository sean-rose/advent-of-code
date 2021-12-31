#!/usr/bin/env python

from __future__ import annotations
from collections import OrderedDict
from pathlib import Path
from typing import Optional


FILE_PATH = Path(__file__)

ADJASCENT_DIFFS = (
              (0, -1),
    (-1,  0),          (1,  0),
              (0,  1)
)


class Point:
    def __init__(self, x: int, y: int, risk_level: int) -> None:
        self.x = x
        self.y = y
        self.risk_level = risk_level

    def __str__(self) -> str:
        return f"({self.x},{self.y})+{self.risk_level}"


class PathPoint:
    def __init__(self, point: Point, previous_path_point: Optional[PathPoint] = None) -> None:
        self.point = point
        self.previous_path_point = previous_path_point
        self.path_risk_level = 0
        if previous_path_point:
            self.path_risk_level = previous_path_point.path_risk_level + point.risk_level

    def __str__(self) -> str:
        path_traceback = []
        path_point = self
        while path_point:
            path_traceback.append(f"{path_point.point} = {path_point.path_risk_level}")
            path_point = path_point.previous_path_point
        
        return '\n'.join(reversed(path_traceback))


def get_adjascent_points(point: Point, points_grid: list[list[Point]]) -> list[Point]:
    return [
        points_grid[point.y + diff_y][point.x + diff_x]
        for diff_x, diff_y in ADJASCENT_DIFFS
        if 0 <= (point.x + diff_x) < len(points_grid[point.y]) and 0 <= (point.y + diff_y) < len(points_grid)
    ]


def find_least_risky_path(points_grid: list[list[Point]]) -> PathPoint:
    start_point = points_grid[0][0]
    end_point = points_grid[-1][-1]
    print(f"Finding path from {start_point} to {end_point}.")

    start_path_point = PathPoint(start_point)
    least_risky_path_to_point: dict[Point, PathPoint] = {
        start_point: start_path_point
    }
    paths_to_explore: OrderedDict[Point, PathPoint] = OrderedDict({
        adjascent_point: PathPoint(adjascent_point, start_path_point)
        for adjascent_point in get_adjascent_points(start_point, points_grid)
    })
    explored_path_count = 0
    ignored_local_suboptimal_path_count = 0
    ignored_global_suboptimal_path_count = 0

    while paths_to_explore:
        point, path_point = paths_to_explore.popitem()

        if point in least_risky_path_to_point and path_point.path_risk_level >= least_risky_path_to_point[point].path_risk_level:
            ignored_local_suboptimal_path_count += 1
            continue

        if end_point in least_risky_path_to_point:
            path_best_ultimate_risk_level = path_point.path_risk_level + (end_point.x - point.x) + (end_point.y - point.y)
            if path_best_ultimate_risk_level >= least_risky_path_to_point[end_point].path_risk_level:
                ignored_global_suboptimal_path_count += 1
                continue

        least_risky_path_to_point[point] = path_point
        if point == end_point:
            print(f"Found path to end with risk level {path_point.path_risk_level}.")

        for adjascent_point in get_adjascent_points(point, points_grid):
            if adjascent_point != path_point.previous_path_point.point:
                new_path_point = PathPoint(adjascent_point, path_point)
                if adjascent_point in paths_to_explore and new_path_point.path_risk_level >= paths_to_explore[adjascent_point].path_risk_level:
                    ignored_local_suboptimal_path_count += 1
                    continue
                paths_to_explore[adjascent_point] = new_path_point
                if adjascent_point.x < point.x or adjascent_point.y < point.y:
                    paths_to_explore.move_to_end(adjascent_point, last=False)

        explored_path_count += 1
        if explored_path_count % 100000 == 0:
            print(f"Explored {explored_path_count} paths.")

    print(f"Explored {explored_path_count} paths.")
    print(f"Ignored {ignored_local_suboptimal_path_count} locally suboptimal paths.")
    print(f"Ignored {ignored_global_suboptimal_path_count} globally suboptimal paths.")

    return least_risky_path_to_point[end_point]


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        first_tile_points_grid = [
            [Point(x, y, int(risk_level_str)) for x, risk_level_str in enumerate(line.rstrip())]
            for y, line in enumerate(file)
        ]

    tile_height = len(first_tile_points_grid)
    tile_width = len(first_tile_points_grid[0])
    first_tile_least_risky_path = find_least_risky_path(first_tile_points_grid)
    print(f"Least risky path for first {tile_width}x{tile_height} tile:\n{first_tile_least_risky_path}")

    points_grid = [
        [
            Point(
                x,
                y,
                (((first_tile_points_grid[y % tile_height][x % tile_width].risk_level + (x // tile_width) + (y // tile_height) - 1) % 9) + 1)
            )
            for x in range(5 * tile_width)
        ]
        for y in range(5 * tile_height)
    ]
    area_height = len(points_grid)
    area_width = len(points_grid[0])
    print(f"Full area is {area_width}x{area_height}.")

    least_risky_path = find_least_risky_path(points_grid)
    print(f"Least risky path for full {area_width}x{area_height} area:\n{least_risky_path}")
