#!/usr/bin/env python

from pathlib import Path
import statistics


FILE_PATH = Path(__file__)


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        crabs = [int(number_str) for number_str in file.readline().rstrip().split(',')]

    possible_positions = list(range(max(crabs) + 1))
    fuel_usage_by_position = {
        position: sum(abs(position - crab_position) for crab_position in crabs)
        for position in possible_positions
    }
    optimal_position = min(possible_positions, key=lambda position: fuel_usage_by_position[position])
    optimal_fuel_usage = fuel_usage_by_position[optimal_position]
    print(f"Optimal position:  {optimal_position}")
    print(f"Fuel usage:  {optimal_fuel_usage}")
