#!/usr/bin/env python

from pathlib import Path
import re


FILE_PATH = Path(__file__)


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"


class Velocity:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"<{self.x},{self.y}>"


class Area:
    def __init__(self, x_range: tuple[int, int], y_range: tuple[int, int]) -> None:
        self.top_left = Point(x_range[0], y_range[1])
        self.bottom_right = Point(x_range[1], y_range[0])

    def __str__(self) -> str:
        return f"{self.top_left}..{self.bottom_right}"

    def contains_point(self, point: Point) -> bool:
        return (
            (self.top_left.x <= point.x <= self.bottom_right.x)
            and (self.bottom_right.y <= point.y <= self.top_left.y)
        )


class Probe:
    def __init__(self, position: Point, velocity: Velocity) -> None:
        self.position = position
        self.velocity = velocity

    def __str__(self) -> str:
        return f"{self.position}+{self.velocity}"

    def move(self) -> None:
        self.position = Point(self.position.x + self.velocity.x, self.position.y + self.velocity.y)
        self.velocity = Velocity(max(self.velocity.x - 1, 0), self.velocity.y - 1)


def aim_to_maximize_height(target_area: Area) -> Velocity:
    initial_x_velocity = 0
    projected_x_distance = 0
    while projected_x_distance < target_area.top_left.x:
        initial_x_velocity += 1
        projected_x_distance += initial_x_velocity

    initial_y_velocity = abs(target_area.bottom_right.y) - 1

    return Velocity(initial_x_velocity, initial_y_velocity)


def fire_probe_at_target_area(initial_velocity: Velocity, target_area: Area) -> list[Point]:
    probe = Probe(Point(0, 0), initial_velocity)
    print(f"Firing probe {probe} at target {target_area}.")
    step = 0
    probe_positions: list[Point] = []
    while (
        not target_area.contains_point(probe.position)
        and probe.position.x <= target_area.bottom_right.x
        and probe.position.y >= target_area.bottom_right.y
    ):
        step += 1
        probe.move()
        probe_positions.append(probe.position)
        print(f"{step}: {probe}")

    if target_area.contains_point(probe.position):
        print("Hit the target!")
    else:
        print("Missed the target.")

    return probe_positions


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        line = file.readline().rstrip()
        match = re.match(r'target area: *x=(-?\d+)\.\.(-?\d+), *y=(-?\d+)\.\.(-?\d+)', line)
        target_area = Area((int(match[1]), int(match[2])), (int(match[3]), int(match[4])))

    print(f"Target area:  {target_area}")

    initial_velocity = aim_to_maximize_height(target_area)
    probe_positions = fire_probe_at_target_area(initial_velocity, target_area)
    max_probe_height = max(position.y for position in probe_positions)
    print(f"Max probe height:  {max_probe_height}")
