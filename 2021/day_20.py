#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


class ImageEnhancementAlgorithm:
    def __init__(self, source: str) -> None:
        self.source = source


class Image:
    def __init__(self, lines: list[str], default_pixel: str = '.') -> None:
        self.lines = lines
        self.default_pixel = default_pixel

    def __str__(self) -> str:
        return '\n'.join(self.lines)

    def get_pixel(self, x: int, y: int) -> str:
        if 0 <= x < len(self.lines[0]) and 0 <= y < len(self.lines):
            return self.lines[y][x]
        else:
            return self.default_pixel

    def get_pixels(self, x_start: int, y_start: int, x_end: int, y_end: int) -> list[str]:
        return [
            ''.join(self.get_pixel(x, y) for x in range(x_start, x_end + 1))
            for y in range(y_start, y_end + 1)
        ]


def enhance_pixels(pixels: list[str], algorithm: str) -> str:
    pixels_str = ''.join(row for row in pixels)
    return algorithm[sum((2 ** index if pixel == '#' else 0) for index, pixel in enumerate(reversed(pixels_str)))]


def enhance_image(image: Image, algorithm: str) -> Image:
    new_lines = [
        ''.join(
            enhance_pixels(image.get_pixels(x - 1, y - 1, x + 1, y + 1), algorithm)
            for x in range(-1, len(image.lines[0]) + 1)
        )
        for y in range(-1, len(image.lines) + 1)
    ]
    all_default_pixels = [image.default_pixel * 3] * 3
    new_default_pixel = enhance_pixels(all_default_pixels, algorithm)
    return Image(new_lines, new_default_pixel)


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        image_enhancement_algorithm = file.readline().rstrip()
        image_lines = [line for line in (full_line.rstrip() for full_line in file) if line]

    image = Image(image_lines)
    print(image)
    for step in range(1,3):
        image = enhance_image(image, image_enhancement_algorithm)
        print(f"\nEnhancement {step}:\n{image}")

    print(f"\nPixels lit:  {str(image).count('#')}")
