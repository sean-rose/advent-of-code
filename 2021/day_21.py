#!/usr/bin/env python

import itertools
from pathlib import Path
import re


FILE_PATH = Path(__file__)


class Player:
    def __init__(self, number: int, position: int) -> None:
        self.number = number
        self.position = position
        self.score = 0


class DeterministicDie:
    def __init__(self, sides: int) -> None:
        self.sides = sides
        self.next_roll = 1

    def roll(self) -> int:
        roll = self.next_roll
        self.next_roll = (roll % self.sides) + 1
        return roll


if __name__ == '__main__':
    players: list[Player] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        for line in file:
            if match := re.match(r'Player (\d+) starting position: *(\d+)', line):
                players.append(Player(int(match[1]), int(match[2])))

    die = DeterministicDie(100)
    roll_count = 0
    for current_player in itertools.cycle(players):
        roll_total = sum(die.roll() for _ in range(3))
        roll_count += 3
        current_player.position = ((current_player.position + roll_total - 1) % 10) + 1
        current_player.score += current_player.position
        if current_player.score >= 1000:
            print(f"Player {current_player.number} won after {roll_count} rolls with score {current_player.score}.")
            losing_player = [player for player in players if player != current_player][0]
            print(f"Player {losing_player.number} lost with score {losing_player.score}.")
            print(f"Losing score multiplied by die rolls:  {losing_player.score * roll_count}")
            break
