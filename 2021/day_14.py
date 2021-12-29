#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path


FILE_PATH = Path(__file__)


def polymerize(polymer: str, pair_insertion_rules: dict[str, str]) -> str:
    new_polymer = polymer[0]
    for index in range(0, len(polymer) - 1):
        pair = polymer[index:index + 2]
        if pair in pair_insertion_rules:
            new_polymer += pair_insertion_rules[pair]
        new_polymer += pair[1]
    return new_polymer


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        polymer_template = file.readline().rstrip()
        pair_insertion_rules: dict[str, str] = {}
        for line in file:
            if ' -> ' in line:
                pair, _, insertion = line.rstrip().split()
                pair_insertion_rules[pair] = insertion

    print(f"Template:  {polymer_template}")
    polymer = polymer_template
    for step in range(1, 11):
        polymer = polymerize(polymer, pair_insertion_rules)
        print(f"Elements after step {step}:  {len(polymer)}")
    
    element_counts = defaultdict(int)
    for element in polymer:
        element_counts[element] += 1

    most_common_element = max(element_counts, key=lambda element: element_counts[element])
    most_common_element_count = element_counts[most_common_element]
    print(f"Most common element:  {most_common_element} ({most_common_element_count})")

    least_common_element = min(element_counts, key=lambda element: element_counts[element])
    least_common_element_count = element_counts[least_common_element]
    print(f"Least common element:  {least_common_element} ({least_common_element_count})")

    most_least_common_element_diff = most_common_element_count - least_common_element_count
    print(f"Difference between most & least common elements:  {most_least_common_element_diff}")
