#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path


FILE_PATH = Path(__file__)


def diagnose_power_consumption(binary_numbers: list[str]) -> int:
    bit_counts = [defaultdict(int) for _ in range(len(binary_numbers[0]))]

    for binary_number in binary_numbers:
        for index, bit in enumerate(binary_number):
            bit_counts[index][bit] += 1

    gamma_rate_binary = ''
    epsilon_rate_binary = ''
    for bit_count in bit_counts:
        gamma_rate_binary   += '0' if bit_count['0'] > bit_count['1'] else '1'
        epsilon_rate_binary += '0' if bit_count['0'] < bit_count['1'] else '1'

    gamma_rate = int(gamma_rate_binary, 2)
    print(f"Gamma rate:  {gamma_rate} ({gamma_rate_binary})")

    epsilon_rate = int(epsilon_rate_binary, 2)
    print(f"Epsilon rate:  {epsilon_rate} ({epsilon_rate_binary})")

    return gamma_rate * epsilon_rate


def partition_by_bit(bit_index: int, binary_numbers: list[str]) -> dict[str, list[str]]:
    partitions = defaultdict(list)
    for binary_number in binary_numbers:
        partitions[binary_number[bit_index]].append(binary_number)
    return partitions


def diagnose_life_support_rating(binary_numbers: list[str]) -> int:
    possible_oxygen_generator_ratings = binary_numbers
    for bit_index in range(len(possible_oxygen_generator_ratings[0])):
        partitions = partition_by_bit(bit_index, possible_oxygen_generator_ratings)
        possible_oxygen_generator_ratings = partitions['1'] if len(partitions['1']) >= len(partitions['0']) else partitions['0']
        if len(possible_oxygen_generator_ratings) == 1:
            oxygen_generator_rating_binary = possible_oxygen_generator_ratings[0]
            oxygen_generator_rating = int(oxygen_generator_rating_binary, 2)
            print(f"Oxygen generator rating:  {oxygen_generator_rating} ({oxygen_generator_rating_binary})")
            break
    else:
        raise Exception("Didn't find an oxygen generator rating.")

    possible_co2_scrubber_ratings = binary_numbers
    for bit_index in range(len(possible_co2_scrubber_ratings[0])):
        partitions = partition_by_bit(bit_index, possible_co2_scrubber_ratings)
        possible_co2_scrubber_ratings = partitions['0'] if len(partitions['0']) <= len(partitions['1']) else partitions['1']
        if len(possible_co2_scrubber_ratings) == 1:
            co2_scrubber_rating_binary = possible_co2_scrubber_ratings[0]
            co2_scrubber_rating = int(co2_scrubber_rating_binary, 2)
            print(f"CO2 scrubber rating:  {co2_scrubber_rating} ({co2_scrubber_rating_binary})")
            break
    else:
        raise Exception("Didn't find a CO2 scrubber rating.")
    
    return oxygen_generator_rating * co2_scrubber_rating


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        binary_numbers = [line.rstrip() for line in file]

    power_consumption = diagnose_power_consumption(binary_numbers)
    print(f"Power consumption:  {power_consumption}")

    life_support_rating = diagnose_life_support_rating(binary_numbers)
    print(f"Life support rating:  {life_support_rating}")
