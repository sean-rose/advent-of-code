#!/usr/bin/env python

from __future__ import annotations
from pathlib import Path
import re
from typing import Optional


FILE_PATH = Path(__file__)


class Cube:
    def __init__(self, x_range: tuple[int, int], y_range: tuple[int, int], z_range: tuple[int, int]) -> None:
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    @property
    def volume(self) -> int:
        return (
            (self.x_range[1] - self.x_range[0] + 1)
            * (self.y_range[1] - self.y_range[0] + 1)
            * (self.z_range[1] - self.z_range[0] + 1)
        )

    def intersection(self, other: Cube) -> Optional[Cube]:
        if (
            self.x_range[0] <= other.x_range[1]
            and self.x_range[1] >= other.x_range[0]
            and self.y_range[0] <= other.y_range[1]
            and self.y_range[1] >= other.y_range[0]
            and self.z_range[0] <= other.z_range[1]
            and self.z_range[1] >= other.z_range[0]
        ):
            return Cube(
                (max(self.x_range[0], other.x_range[0]), min(self.x_range[1], other.x_range[1])),
                (max(self.y_range[0], other.y_range[0]), min(self.y_range[1], other.y_range[1])),
                (max(self.z_range[0], other.z_range[0]), min(self.z_range[1], other.z_range[1]))
            )
        else:
            return None


class RebootStep:
    def __init__(self, on: bool, region: Cube) -> None:
        self.on = on
        self.region = region


class Reactor:
    def __init__(self) -> None:
        self.on_regions: list[Cube] = []

    def do_reboot_step(self, step: RebootStep) -> None:
        new_region = step.region
        new_on_regions: list[Cube] = []
        for existing_region in self.on_regions:
            if new_region.intersection(existing_region):
                if existing_region.x_range[0] < new_region.x_range[0]:
                    disjoint_region = Cube((existing_region.x_range[0], new_region.x_range[0] - 1), existing_region.y_range, existing_region.z_range)
                    existing_region = Cube((new_region.x_range[0], existing_region.x_range[1]), existing_region.y_range, existing_region.z_range)
                    new_on_regions.append(disjoint_region)
                if existing_region.x_range[1] > new_region.x_range[1]:
                    disjoint_region = Cube((new_region.x_range[1] + 1, existing_region.x_range[1]), existing_region.y_range, existing_region.z_range)
                    existing_region = Cube((existing_region.x_range[0], new_region.x_range[1]), existing_region.y_range, existing_region.z_range)
                    new_on_regions.append(disjoint_region)

                if existing_region.y_range[0] < new_region.y_range[0]:
                    disjoint_region = Cube(existing_region.x_range, (existing_region.y_range[0], new_region.y_range[0] - 1), existing_region.z_range)
                    existing_region = Cube(existing_region.x_range, (new_region.y_range[0], existing_region.y_range[1]), existing_region.z_range)
                    new_on_regions.append(disjoint_region)
                if existing_region.y_range[1] > new_region.y_range[1]:
                    disjoint_region = Cube(existing_region.x_range, (new_region.y_range[1] + 1, existing_region.y_range[1]), existing_region.z_range)
                    existing_region = Cube(existing_region.x_range, (existing_region.y_range[0], new_region.y_range[1]), existing_region.z_range)
                    new_on_regions.append(disjoint_region)

                if existing_region.z_range[0] < new_region.z_range[0]:
                    disjoint_region = Cube(existing_region.x_range, existing_region.y_range, (existing_region.z_range[0], new_region.z_range[0] - 1))
                    existing_region = Cube(existing_region.x_range, existing_region.y_range, (new_region.z_range[0], existing_region.z_range[1]))
                    new_on_regions.append(disjoint_region)
                if existing_region.z_range[1] > new_region.z_range[1]:
                    disjoint_region = Cube(existing_region.x_range, existing_region.y_range, (new_region.z_range[1] + 1, existing_region.z_range[1]))
                    existing_region = Cube(existing_region.x_range, existing_region.y_range, (existing_region.z_range[0], new_region.z_range[1]))
                    new_on_regions.append(disjoint_region)
            else:
                new_on_regions.append(existing_region)

        if step.on:
            new_on_regions.append(new_region)

        self.on_regions = new_on_regions


if __name__ == '__main__':
    reboot_steps: list[RebootStep] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        for line in file:
            if match := re.match(r'(on|off) *x=([-\d]+)\.\.([-\d]+),y=([-\d]+)\.\.([-\d]+),z=([-\d]+)\.\.([-\d]+)', line):
                on = match[1] == 'on'
                region = Cube((int(match[2]), int(match[3])), (int(match[4]), int(match[5])), (int(match[6]), int(match[7])))
                reboot_steps.append(RebootStep(on, region))

    reactor = Reactor()
    for step in reboot_steps:
        reactor.do_reboot_step(step)

    initialization_region = Cube((-50, 50), (-50, 50), (-50, 50))
    initialization_on_regions = [
        initialization_on_region
        for initialization_on_region in (on_region.intersection(initialization_region) for on_region in reactor.on_regions)
        if initialization_on_region
    ]
    initialization_on_volume = sum(region.volume for region in initialization_on_regions)
    print(f"Cubes on in initialization region:  {initialization_on_volume}")
