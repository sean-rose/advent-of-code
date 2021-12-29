#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path


FILE_PATH = Path(__file__)


class Polymer:
    def __init__(self, initial_elements: str, element_pair_insertion_rules: dict[str, str]) -> None:
        self.initial_elements = initial_elements
        self.first_element = initial_elements[0]
        self.last_element = initial_elements[-1]
        self.element_pair_counts: dict[str, int] = defaultdict(int)
        for index in range(0, len(initial_elements) - 1):
            self.element_pair_counts[initial_elements[index:index + 2]] += 1
        self.element_pair_insertion_rules = element_pair_insertion_rules

    def polymerize(self) -> None:
        current_element_pair_counts = self.element_pair_counts.copy()
        for element_pair in current_element_pair_counts:
            if element_pair in self.element_pair_insertion_rules:
                current_element_pair_count = current_element_pair_counts[element_pair]
                inserted_element = self.element_pair_insertion_rules[element_pair]
                self.element_pair_counts[element_pair[0] + inserted_element] += current_element_pair_count
                self.element_pair_counts[inserted_element + element_pair[1]] += current_element_pair_count
                self.element_pair_counts[element_pair] -= current_element_pair_count

    def count_elements(self) -> dict[str, int]:
        element_counts: dict[str, int] = defaultdict(int)
        for element_pair in self.element_pair_counts:
            element_counts[element_pair[0]] += self.element_pair_counts[element_pair]
        element_counts[self.last_element] += 1
        return element_counts


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        polymer_template = file.readline().rstrip()
        element_pair_insertion_rules: dict[str, str] = {}
        for line in file:
            if ' -> ' in line:
                element_pair, _, inserted_element = line.rstrip().split()
                element_pair_insertion_rules[element_pair] = inserted_element

    print(f"Template:  {polymer_template}")
    polymer = Polymer(polymer_template, element_pair_insertion_rules)
    for step in range(1, 41):
        polymer.polymerize()
        element_counts = polymer.count_elements()
        print(f"Elements after step {step}:  {sum(element_counts.values())}")

        if step in (10, 40):
            most_common_element = max(element_counts, key=lambda element: element_counts[element])
            most_common_element_count = element_counts[most_common_element]
            print(f"Most common element after step {step}:  {most_common_element} ({most_common_element_count})")

            least_common_element = min(element_counts, key=lambda element: element_counts[element])
            least_common_element_count = element_counts[least_common_element]
            print(f"Least common element after step {step}:  {least_common_element} ({least_common_element_count})")

            most_least_common_element_diff = most_common_element_count - least_common_element_count
            print(f"Difference between most & least common elements after step {step}:  {most_least_common_element_diff}")
