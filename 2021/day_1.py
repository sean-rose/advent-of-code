#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


def count_depth_increases(depths: list[int]) -> int:
    depth_increases_count = 0
    previous_depth = None

    for depth in depths:
        if previous_depth is not None and depth > previous_depth:
            depth_increases_count += 1
        previous_depth = depth

    return depth_increases_count


def count_sliding_window_depth_increases(depths: list[int]) -> int:
    depth_increases_count = 0

    for index in range(3, len(depths)):
        if sum(depths[index-2:index+1]) > sum(depths[index-3:index]):
            depth_increases_count += 1

    return depth_increases_count


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        depths = [int(line) for line in file]

    print(f"Depth increases:  {count_depth_increases(depths)}")
    print(f"Sliding window depth increases:  {count_sliding_window_depth_increases(depths)}")
