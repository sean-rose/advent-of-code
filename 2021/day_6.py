#!/usr/bin/env python

import functools
from pathlib import Path


FILE_PATH = Path(__file__)


@functools.lru_cache(maxsize=None)
def simulate_population_growth(days_until_reproduction: int, simulate_days: int) -> int:
    population = 1
    while simulate_days > days_until_reproduction:
        simulate_days -= days_until_reproduction + 1
        population += simulate_population_growth(8, simulate_days)
        days_until_reproduction = 6
    return population


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        fish = [int(number_str) for number_str in file.readline().rstrip().split(',')]

    fish_after_80_days = sum(simulate_population_growth(days_until_reproduction, 80) for days_until_reproduction in fish)
    print(f"Fish after 80 days:  {fish_after_80_days}")

    fish_after_256_days = sum(simulate_population_growth(days_until_reproduction, 256) for days_until_reproduction in fish)
    print(f"Fish after 256 days:  {fish_after_256_days}")
