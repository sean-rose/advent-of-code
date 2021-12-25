#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        current_fish = [int(number_str) for number_str in file.readline().rstrip().split(',')]

    for day in range(1, 81):
        new_fish = []
        for index, fish in enumerate(current_fish):
            if fish == 0:
                new_fish.append(8)
                current_fish[index] = 6
            else:
                current_fish[index] = fish - 1
        current_fish.extend(new_fish)

    print(f"Fish after 80 days:  {len(current_fish)}")
