#!/usr/bin/env python

from pathlib import Path
from typing import Optional


FILE_PATH = Path(__file__)

OPEN_CHARS  = '([{<'
CLOSE_CHARS = ')]}>'

ILLEGAL_CHAR_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def find_illegal_char(line: str) -> Optional[str]:
    stack: list[str] = []
    for index, char in enumerate(line):
        if char in OPEN_CHARS:
            stack.append(char)
        elif char in CLOSE_CHARS:
            expected_char = CLOSE_CHARS[OPEN_CHARS.index(stack[-1])]
            if char == expected_char:
                stack.pop()
            else:
                print(f"{line[:index + 1]} - Expected {expected_char}, but found {char} instead.")
                return char
    return None


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        lines = [line.rstrip() for line in file]

    illegal_chars = [char for char in [find_illegal_char(line) for line in lines] if char]
    syntax_error_score = sum(ILLEGAL_CHAR_POINTS[char] for char in illegal_chars)
    print(f"Syntax error score:  {syntax_error_score}")
