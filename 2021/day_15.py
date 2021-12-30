#!/usr/bin/env python

from collections import deque
from pathlib import Path


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

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"({self.x},{self.y})+{self.risk_level}"


class Path:
    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.risk_level = sum(point.risk_level for point in points[1:])

    def __str__(self) -> str:
        lines = [str(self.points[0])]
        cumulative_risk_level = 0
        for point in self.points[1:]:
            cumulative_risk_level += point.risk_level
            lines.append(f"{point} = {cumulative_risk_level}")
        return '\n'.join(lines)


def get_adjascent_points(point: Point, risk_levels: list[list[Point]]) -> list[Point]:
    return [
        risk_levels[point.y + diff_y][point.x + diff_x]
        for diff_x, diff_y in ADJASCENT_DIFFS
        if 0 <= (point.x + diff_x) < len(risk_levels[point.y]) and 0 <= (point.y + diff_y) < len(risk_levels)
    ]


def find_least_risky_path(risk_levels: list[list[Point]]) -> Path:
    start_point = risk_levels[0][0]
    end_point = risk_levels[-1][-1]
    least_risky_path_to_point: dict[Point, Path] = {
        start_point: Path([start_point])
    }
    points_to_explore = deque(get_adjascent_points(start_point, risk_levels))

    while points_to_explore:
        point = points_to_explore.popleft()
        adjascent_points = get_adjascent_points(point, risk_levels)
        adjascent_paths = [
            least_risky_path_to_point[adjascent_point]
            for adjascent_point in adjascent_points
            if adjascent_point in least_risky_path_to_point and point not in least_risky_path_to_point[adjascent_point].points
        ]
        if adjascent_paths:
            adjascent_paths.sort(key=lambda path: path.risk_level)
            new_path_to_point = Path(adjascent_paths[0].points + [point])
            if point not in least_risky_path_to_point or new_path_to_point.risk_level < least_risky_path_to_point[point].risk_level:
                least_risky_path_to_point[point] = new_path_to_point
                points_to_explore.extend(
                    adjascent_point
                    for adjascent_point in adjascent_points
                    if adjascent_point not in new_path_to_point.points
                )

    return least_risky_path_to_point[end_point]


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        risk_levels = [
            [Point(x, y, int(risk_level_str)) for x, risk_level_str in enumerate(line.rstrip())]
            for y, line in enumerate(file)
        ]

    least_risky_path = find_least_risky_path(risk_levels)
    print(f"Least risky path:\n{least_risky_path}")
