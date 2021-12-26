#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)

'''
 aaaa
b    c
b    c
 dddd
e    f
e    f
 gggg
'''
DIGIT_SIGNAL_PATTERNS = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9
}


'''
Segment frequencies (digits they appear in):
    a = 8  (0   2 3   5 6 7 8 9)
    b = 6  (0       4 5 6   8 9)
    c = 8  (0 1 2 3 4     7 8 9)
    d = 7  (    2 3 4 5 6   8 9)
    e = 4  (0   2       6   8  )
    f = 9  (0 1   3 4 5 6 7 8 9)
    g = 7  (0   2 3   5 6   8 9)
'''
def decode_display(unique_signal_patterns: list[str], display_patterns: list[str]):
    signal_corrections = {}
    unique_signal_patterns = [''.join(pattern) for pattern in unique_signal_patterns]
    signal_frequencies = {signal: sum(1 for pattern in unique_signal_patterns if signal in pattern) for signal in 'abcdefg'}
    for signal, frequency in signal_frequencies.items():
        if frequency == 6:
            signal_corrections[signal] = 'b'
        elif frequency == 4:
            signal_corrections[signal] = 'e'
        elif frequency == 9:
            signal_corrections[signal] = 'f'
    one_pattern = [pattern for pattern in unique_signal_patterns if len(pattern) == 2][0]
    for signal in one_pattern:
        if signal not in signal_corrections:
            signal_corrections[signal] = 'c'
            break
    seven_pattern = [pattern for pattern in unique_signal_patterns if len(pattern) == 3][0]
    for signal in seven_pattern:
        if signal not in one_pattern:
            signal_corrections[signal] = 'a'
            break
    four_pattern = [pattern for pattern in unique_signal_patterns if len(pattern) == 4][0]
    for signal in four_pattern:
        if signal not in signal_corrections:
            signal_corrections[signal] = 'd'
            break
    for signal in 'abcdefg':
        if signal not in signal_corrections:
            signal_corrections[signal] = 'g'
            break
    corrected_display_patterns = [''.join(sorted(signal_corrections[signal] for signal in pattern)) for pattern in display_patterns]
    return [DIGIT_SIGNAL_PATTERNS[pattern] for pattern in corrected_display_patterns]


if __name__ == '__main__':
    display_digits: list[list[int]] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        for line in file.readlines():
            unique_signal_patterns, output = [[pattern for pattern in part.split()] for part in line.rstrip().split('|')]
            display_digits.append(decode_display(unique_signal_patterns, output))

    count_of_1478 = sum(sum(1 for digit in digits if digit in (1, 4, 7, 8)) for digits in display_digits)
    print(f"How many times digits 1, 4, 7, or 8 appear:  {count_of_1478}")
