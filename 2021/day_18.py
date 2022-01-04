#!/usr/bin/env python

from __future__ import annotations
import math
from pathlib import Path
from typing import Optional, Union


FILE_PATH = Path(__file__)


class SnailfishNumber:
    def __init__(self, left: Union[int, SnailfishNumber], right: Union[int, SnailfishNumber]) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        result = SnailfishNumber(self, other)
        result.reduce()
        return result

    @property
    def magnitude(self) -> int:
        left_magnitude = self.left.magnitude if isinstance(self.left, SnailfishNumber) else self.left
        right_magnitude = self.right.magnitude if isinstance(self.right, SnailfishNumber) else self.right
        return (left_magnitude * 3) + (right_magnitude * 2)

    @classmethod
    def from_string(cls, source: str) -> SnailfishNumber:
        if source[1] == '[':
            open_brackets = 1
            closing_bracket_search_index = 1
            while open_brackets > 0:
                closing_bracket_search_index += 1
                if source[closing_bracket_search_index] == '[':
                    open_brackets += 1
                elif source[closing_bracket_search_index] == ']':
                    open_brackets -= 1
            left_string = source[1:closing_bracket_search_index + 1]
            left = cls.from_string(left_string)
        elif source[1].isdigit():
            non_digit_search_offset = 2
            while source[non_digit_search_offset].isdigit():
                non_digit_search_offset += 1
            left_string = source[1:non_digit_search_offset]
            left = int(left_string)
        else:
            raise Exception(f"Couldn't parse snailfish number:  {source}")

        end_index = source.rindex(']')
        right_string = source[len(left_string) + 2:end_index]
        if right_string[0] == '[':
            right = cls.from_string(right_string)
        elif right_string.isdigit():
            right = int(right_string)
        else:
            raise Exception(f"Couldn't parse snailfish number:  {source}")

        return SnailfishNumber(left, right)

    def reduce(self) -> None:
        while True:
            if self.explode():
                continue
            elif self.split():
                continue
            else:
                break

    def index(self, parent: Optional[SnailfishNumberIndex] = None, depth: int = 1) -> list[SnailfishNumberIndex]:
        indexes: list[SnailfishNumber] = []
        index = SnailfishNumberIndex(self, parent, depth)
        if isinstance(self.left, SnailfishNumber):
            indexes.extend(self.left.index(index, depth + 1))
        indexes.append(index)
        if isinstance(self.right, SnailfishNumber):
            indexes.extend(self.right.index(index, depth + 1))
        return indexes

    def explode(self) -> bool:
        indexes = self.index()
        for i, index in enumerate(indexes):
            if index.depth > 4:
                for previous_index in reversed(indexes[:i]):
                    if isinstance(previous_index.number.right, int):
                        previous_index.number.right += index.number.left
                        break
                    elif isinstance(previous_index.number.left, int):
                        previous_index.number.left += index.number.left
                        break
                for next_index in indexes[i + 1:]:
                    if isinstance(next_index.number.left, int):
                        next_index.number.left += index.number.right
                        break
                    elif isinstance(next_index.number.right, int):
                        next_index.number.right += index.number.right
                        break
                if index.parent.number.left is index.number:
                    index.parent.number.left = 0
                elif index.parent.number.right is index.number:
                    index.parent.number.right = 0
                return True
        return False

    def split(self) -> bool:
        if isinstance(self.left, int) and self.left >= 10:
            self.left = SnailfishNumber(math.floor(self.left / 2), math.ceil(self.left /2))
            return True
        elif isinstance(self.left, SnailfishNumber) and self.left.split():
            return True
        elif isinstance(self.right, int) and self.right >= 10:
            self.right = SnailfishNumber(math.floor(self.right / 2), math.ceil(self.right /2))
            return True
        elif isinstance(self.right, SnailfishNumber) and self.right.split():
            return True
        return False


class SnailfishNumberIndex:
    def __init__(self, number: SnailfishNumber, parent: SnailfishNumberIndex, depth: int) -> None:
        self.number = number
        self.parent = parent
        self.depth = depth


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        snailfish_numbers = [SnailfishNumber.from_string(line.rstrip()) for line in file]

    total = snailfish_numbers[0]
    for snailfish_number in snailfish_numbers[1:]:
        print(f"\n  {total}")
        print(f"+ {snailfish_number}")
        total = total + snailfish_number
        print(f"= {total} ({total.magnitude})")
