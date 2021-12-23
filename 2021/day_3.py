#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path


FILE_PATH = Path(__file__)


def diagnose_submarine(binary_numbers: list[str]) -> tuple[str, str]:
    bit_counts = [defaultdict(int) for _ in range(len(binary_numbers[0]))]

    for binary_number in binary_numbers:
        for index, bit in enumerate(binary_number):
            bit_counts[index][bit] += 1

    gamma_rate_binary = ''
    epsilon_rate_binary = ''
    for bit_count in bit_counts:
        gamma_rate_binary   += '0' if bit_count['0'] > bit_count['1'] else '1'
        epsilon_rate_binary += '0' if bit_count['0'] < bit_count['1'] else '1'

    return gamma_rate_binary, epsilon_rate_binary


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        binary_numbers = [line.rstrip() for line in file]

    gamma_rate_binary, epsilon_rate_binary = diagnose_submarine(binary_numbers)
    gamma_rate = int(gamma_rate_binary, 2)
    epsilon_rate = int(epsilon_rate_binary, 2)
    power_consumption = gamma_rate * epsilon_rate

    print(f"Gamma rate:  {gamma_rate} ({gamma_rate_binary})")
    print(f"Epsilon rate:  {epsilon_rate} ({epsilon_rate_binary})")
    print(f"Power consumption:  {power_consumption}")
