#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


def triangular_number(number: int) -> int:
    return (number * (number + 1)) // 2


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        crabs = [int(number_str) for number_str in file.readline().rstrip().split(',')]

    possible_positions = list(range(max(crabs) + 1))

    naive_fuel_usage_by_position = {
        position: sum(abs(position - crab_position) for crab_position in crabs)
        for position in possible_positions
    }
    naive_optimal_position = min(possible_positions, key=lambda position: naive_fuel_usage_by_position[position])
    naive_optimal_fuel_usage = naive_fuel_usage_by_position[naive_optimal_position]
    print(f"Naive optimal position:  {naive_optimal_position}")
    print(f"Naive fuel usage:  {naive_optimal_fuel_usage}")

    actual_fuel_usage_by_position = {
        position: sum(triangular_number(abs(position - crab_position)) for crab_position in crabs)
        for position in possible_positions
    }
    actual_optimal_position = min(possible_positions, key=lambda position: actual_fuel_usage_by_position[position])
    actual_optimal_fuel_usage = actual_fuel_usage_by_position[actual_optimal_position]
    print(f"Actual optimal position:  {actual_optimal_position}")
    print(f"Actual fuel usage:  {actual_optimal_fuel_usage}")
