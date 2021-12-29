#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


class Paper:
    def __init__(self, dot_coordinates: list[tuple[int, int]]) -> None:
        max_x = max(dot_coordinate[0] for dot_coordinate in dot_coordinates)
        max_y = max(dot_coordinate[1] for dot_coordinate in dot_coordinates)
        self.dots = [[False for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for dot_x, dot_y in dot_coordinates:
            self.dots[dot_y][dot_x] = True

    def count_dots(self) -> int:
        return sum(1 for row in self.dots for has_dot in row if has_dot)

    def fold(self, axis: str, distance: int) -> None:
        if axis == 'x':
            new_dots = [row[:distance] for row in self.dots]
            for dot_y in range(0, len(self.dots)):
                for dot_x in range(distance + 1, len(self.dots[dot_y])):
                    if self.dots[dot_y][dot_x]:
                        new_dots[dot_y][distance - (dot_x - distance)] = True
        elif axis == 'y':
            new_dots = self.dots[:distance]
            for dot_y in range(distance + 1, len(self.dots)):
                for dot_x in range(len(self.dots[dot_y])):
                    if self.dots[dot_y][dot_x]:
                        new_dots[distance - (dot_y - distance)][dot_x] = True
        else:
            raise Exception(f"Unkown axis:  {axis}")

        self.dots = new_dots

    def __str__(self) -> str:
        return '\n'.join(''.join('#' if has_dot else '.' for has_dot in row) for row in self.dots)


if __name__ == '__main__':
    dot_coordinates: list[tuple[int, int]] = []
    folds: list[tuple[str, int]] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        for line in file:
            if ',' in line:
                dot_coordinates.append(tuple(int(coordinate) for coordinate in line.rstrip().split(',')))
            elif line.startswith('fold along '):
                axis, distance_str = line[11:].rstrip().split('=')
                folds.append((axis, int(distance_str)))

    paper = Paper(dot_coordinates)
    print(f"Dots count:  {paper.count_dots()}")
    for axis, distance in folds:
        print(f"Fold along {axis}={distance}.")
        paper.fold(axis, distance)
        print(f"Dots count:  {paper.count_dots()}")
    print(paper)
