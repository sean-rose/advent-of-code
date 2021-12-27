#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)

OPEN_CHARS  = '([{<'
CLOSE_CHARS = ')]}>'

ILLEGAL_CHAR_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

AUTOCOMPLETE_CHAR_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


class IllegalCharError(Exception):
    def __init__(self, input: str, expected_char: str, illegal_char: str) -> None:
        super().__init__(f"{input} - Expected {expected_char}, but found {illegal_char} instead.")
        self.illegal_char = illegal_char


class IncompleteLineError(Exception):
    def __init__(self, input: str, completion: str) -> None:
        super().__init__(f"{input} - Complete by adding {completion}.")
        self.completion = completion


def validate_line(line: str) -> None:
    stack: list[str] = []
    for index, char in enumerate(line):
        if char in OPEN_CHARS:
            stack.append(char)
        elif char in CLOSE_CHARS:
            expected_char = CLOSE_CHARS[OPEN_CHARS.index(stack[-1])]
            if char == expected_char:
                stack.pop()
            else:
                raise IllegalCharError(line[:index + 1], expected_char, char)
        else:
            raise Exception(f"Unexpected character at position {index + 1}:  {char}")
    if stack:
        completion = ''.join(CLOSE_CHARS[OPEN_CHARS.index(open_char)] for open_char in reversed(stack))
        raise IncompleteLineError(line, completion)


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        lines = [line.rstrip() for line in file]

    illegal_chars: list[str] = []
    line_completions: list[str] = []

    for line in lines:
        try:
            validate_line(line)
        except IllegalCharError as error:
            print(error)
            illegal_chars.append(error.illegal_char)
        except IncompleteLineError as error:
            print(error)
            line_completions.append(error.completion)

    syntax_error_score = sum(ILLEGAL_CHAR_POINTS[char] for char in illegal_chars)
    print(f"Syntax error score:  {syntax_error_score}")

    autocomplete_scores: list[int] = []
    for completion in line_completions:
        autocomplete_score = 0
        for char in completion:
            autocomplete_score = (autocomplete_score * 5) + AUTOCOMPLETE_CHAR_POINTS[char]
        autocomplete_scores.append(autocomplete_score)
    autocomplete_scores.sort()
    middle_autocomplete_score = autocomplete_scores[len(autocomplete_scores) // 2]
    print(f"Middle autocomplete score:  {middle_autocomplete_score}")
