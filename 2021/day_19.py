#!/usr/bin/env python

from pathlib import Path
import re
from typing import Optional


FILE_PATH = Path(__file__)

# (coordinate order), (coordinate polarity)
COORDINATE_ROTATIONS: tuple[tuple[tuple[int, int, int], tuple[int, int, int]]] = (
    ((0, 1, 2), ( 1,  1,  1)),
    ((1, 0, 2), ( 1, -1,  1)),
    ((0, 1, 2), (-1, -1,  1)),
    ((1, 0, 2), (-1,  1,  1)),

    ((0, 1, 2), (-1,  1, -1)),
    ((1, 0, 2), ( 1,  1, -1)),
    ((0, 1, 2), ( 1, -1, -1)),
    ((1, 0, 2), (-1, -1, -1)),

    ((0, 2, 1), ( 1, -1,  1)),
    ((2, 0, 1), (-1, -1,  1)),
    ((0, 2, 1), (-1,  1,  1)),
    ((2, 0, 1), ( 1,  1,  1)),

    ((0, 2, 1), ( 1,  1, -1)),
    ((2, 0, 1), ( 1, -1, -1)),
    ((0, 2, 1), (-1, -1, -1)),
    ((2, 0, 1), (-1,  1, -1)),

    ((2, 1, 0), (-1,  1,  1)),
    ((1, 2, 0), ( 1,  1,  1)),
    ((2, 1, 0), ( 1, -1,  1)),
    ((1, 2, 0), (-1, -1,  1)),

    ((2, 1, 0), ( 1,  1, -1)),
    ((1, 2, 0), ( 1, -1, -1)),
    ((2, 1, 0), (-1, -1, -1)),
    ((1, 2, 0), (-1,  1, -1)),
)


class Scanner:
    def __init__(self, number: int) -> None:
        self.number = number
        self.coordinates: Optional[tuple[int, int, int]] = None
        self.beacon_coordinates: set[tuple[int, int, int]] = set()


def rotate_coordinates_set(
    coordinates_set: set[tuple[int, int, int]],
    coordinate_order: tuple[int, int, int],
    coordinate_polarity: tuple[int, int, int]
) -> set[tuple[int, int, int]]:
    return set(
        (
            coordinates[coordinate_order[0]] * coordinate_polarity[0],
            coordinates[coordinate_order[1]] * coordinate_polarity[1],
            coordinates[coordinate_order[2]] * coordinate_polarity[2]
        )
        for coordinates in coordinates_set
    )


def move_coordinates_set(coordinates_set: set[tuple[int, int, int]], distance: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    return set(
        (coordinates[0] + distance[0], coordinates[1] + distance[1], coordinates[2] + distance[2])
        for coordinates in coordinates_set
    )


def align_scanner(scanner: Scanner, aligned_scanners: list[Scanner]) -> bool:
    possible_beacon_coordinates_sets = (
        rotate_coordinates_set(scanner.beacon_coordinates, coordinate_order, coordinate_polarity)
        for coordinate_order, coordinate_polarity in COORDINATE_ROTATIONS
    )
    for possible_beacon_coordinates_set in possible_beacon_coordinates_sets:
        # We're looking for at least 12 matches, so we can stop looking once there are less than 12 possibilities left.
        reduced_possible_beacon_coordinates_set = set(list(possible_beacon_coordinates_set)[:-11])
        for possible_beacon_coordinates in reduced_possible_beacon_coordinates_set:
            for aligned_scanner in aligned_scanners:
                for aligned_beacon_coordinates in aligned_scanner.beacon_coordinates:
                    possible_offset = (
                        aligned_beacon_coordinates[0] - possible_beacon_coordinates[0],
                        aligned_beacon_coordinates[1] - possible_beacon_coordinates[1],
                        aligned_beacon_coordinates[2] - possible_beacon_coordinates[2]
                    )
                    possible_aligned_beacon_coordinates = move_coordinates_set(possible_beacon_coordinates_set, possible_offset)
                    if len(possible_aligned_beacon_coordinates.intersection(aligned_scanner.beacon_coordinates)) >= 12:
                        scanner.coordinates = possible_offset
                        scanner.beacon_coordinates = possible_aligned_beacon_coordinates
                        print(f"Aligned scanner {scanner.number} at {scanner.coordinates} with scanner {aligned_scanner.number} at {aligned_scanner.coordinates}.")
                        return True
    return False


if __name__ == '__main__':
    scanners: list[Scanner] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        lines = (line.rstrip() for line in file)
        for line in lines:
            if line:
                if match := re.match(r'--- scanner (\d+) ---', line):
                    current_scanner = Scanner(int(match[1]))
                    scanners.append(current_scanner)
                else:
                    current_scanner.beacon_coordinates.add(tuple(int(number_str) for number_str in line.split(',')))

    initial_scanner = scanners[0]
    initial_scanner.coordinates = (0, 0, 0)
    aligned_scanners = [initial_scanner]
    scanners_to_align = list(scanners[1:])
    while scanners_to_align:
        for scanner in scanners_to_align:
            if align_scanner(scanner, aligned_scanners):
                aligned_scanners.append(scanner)
                scanners_to_align.remove(scanner)
                break
        else:
            raise Exception("Failed to align any more scanners.")

    all_beacon_coordinates = set(
        beacon_coordinates
        for scanner in aligned_scanners
        for beacon_coordinates in scanner.beacon_coordinates
    )
    print(f"Beacons count:  {len(all_beacon_coordinates)}")
