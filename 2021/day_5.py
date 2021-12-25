#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path


FILE_PATH = Path(__file__)


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, start_point: Point, end_point: Point) -> None:
        self.start_point = start_point
        self.end_point = end_point

    def get_covered_points(self) -> list[Point]:
        x_increment = 0
        if self.end_point.x != self.start_point.x:
            x_increment = 1 if self.end_point.x > self.start_point.x else -1

        y_increment = 0
        if self.end_point.y != self.start_point.y:
            y_increment = 1 if self.end_point.y > self.start_point.y else -1

        total_increments = max(abs(self.end_point.x - self.start_point.x), abs(self.end_point.y - self.start_point.y))
        return [
            Point(
                (self.start_point.x + (x_increment * increment_number)),
                (self.start_point.y + (y_increment * increment_number))
            )
            for increment_number in range(total_increments + 1)
        ]


def count_vents_per_point(vent_lines: list[Line]) -> dict[int, dict[int, int]]:
    points = defaultdict(lambda: defaultdict(int))
    for line in vent_lines:
        for point in line.get_covered_points():
            points[point.y][point.x] += 1
    return points


if __name__ == '__main__':
    vent_lines: list[Line] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        for line in file.readlines():
            line_parts = line.rstrip().split()
            if line_parts and len(line_parts) == 3:
                start_point = Point(*(int(number_str) for number_str in line_parts[0].split(',')))
                end_point   = Point(*(int(number_str) for number_str in line_parts[2].split(',')))
                vent_lines.append(Line(start_point, end_point))

    horizontal_vertical_vent_lines = [
        line
        for line in vent_lines
        if line.end_point.x == line.start_point.x or line.end_point.y == line.start_point.y
    ]
    horizontal_vertical_vents_per_point = count_vents_per_point(horizontal_vertical_vent_lines)
    multiple_horizontal_vertical_vent_points_count = sum(
        1
        for row in horizontal_vertical_vents_per_point.values()
        for vent_count in row.values()
        if vent_count > 1
    )
    print(f"Points with at least two horizontal or vertical vents:  {multiple_horizontal_vertical_vent_points_count}")
