#!/usr/bin/env python

from collections import defaultdict
import itertools
from pathlib import Path
import re
from typing import Optional


FILE_PATH = Path(__file__)


class Player:
    def __init__(self, number: int, position: int) -> None:
        self.number = number
        self.position = position
        self.score = 0


class DeterministicGame:
    def __init__(self, positions: int, die_sides: int, winning_score: int, player_positions: dict[int, int]) -> None:
        self.positions = positions
        self.die_sides = die_sides
        self.roll_count = 0
        self.next_roll = 1
        self.winning_score = winning_score
        self.players = [Player(player_number, position) for player_number, position in player_positions.items()]
        self.next_player_index = 0

    @property
    def in_progress(self) -> bool:
        return all(player.score < self.winning_score for player in self.players)

    @property
    def winner(self) -> Optional[Player]:
        return next((player for player in self.players if player.score >= self.winning_score), None)

    @property
    def loser(self) -> Optional[Player]:
        return next((player for player in self.players if player.score < self.winning_score), None)

    def roll(self) -> int:
        roll = self.next_roll
        self.roll_count += 1
        self.next_roll = (roll % self.die_sides) + 1
        return roll

    def take_turn(self) -> None:
        player = self.players[self.next_player_index]
        roll_total = self.roll() + self.roll() + self.roll()
        player.position = ((player.position + roll_total - 1) % self.positions) + 1
        player.score += player.position
        self.next_player_index = (self.next_player_index + 1) % len(self.players)


class QuantumGame:
    def __init__(self, positions: int, die_sides: int, winning_score: int, player_positions: dict[int, int]) -> None:
        self.positions = positions
        self.die_sides = die_sides
        self.winning_score = winning_score
        self.turn = 0
        # State is the player number, position, and score for each player, with the next player first.
        initial_state = tuple((player_number, position, 0) for player_number, position in player_positions.items())
        self.universes_per_state = {
            initial_state: 1
        }
        self.wins_per_player = defaultdict(int)

        self.universes_per_roll_total: dict[int, int] = defaultdict(int)
        possible_rolls = itertools.product(range(1, self.die_sides + 1), repeat=3)
        for possible_roll in possible_rolls:
            self.universes_per_roll_total[sum(possible_roll)] += 1

    @property
    def in_progress(self) -> bool:
        return len(self.universes_per_state) > 0

    def take_turn(self) -> None:
        self.turn += 1
        print(f"Taking turn {self.turn} with {len(self.universes_per_state)} existing states for {sum(self.universes_per_state.values())} universes.")
        new_universes_per_state = defaultdict(int)
        for existing_state, existing_universes in self.universes_per_state.items():
            current_player_state = existing_state[0]
            other_players_state = existing_state[1:]
            player_number, existing_position, existing_score = current_player_state
            for roll_total, roll_universes in self.universes_per_roll_total.items():
                new_position = ((existing_position + roll_total - 1) % self.positions) + 1
                new_score = existing_score + new_position
                new_universes = existing_universes * roll_universes
                if new_score >= self.winning_score:
                    self.wins_per_player[player_number] += new_universes
                else:
                    new_state = (*other_players_state, (player_number, new_position, new_score))
                    new_universes_per_state[new_state] += new_universes
        self.universes_per_state = new_universes_per_state


if __name__ == '__main__':
    player_positions: dict[int, int] = {}

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        for line in file:
            if match := re.match(r'Player (\d+) starting position: *(\d+)', line):
                player_positions[int(match[1])] = int(match[2])

    practice_game = DeterministicGame(10, 100, 1000, player_positions)
    while practice_game.in_progress:
        practice_game.take_turn()
    practice_winner = practice_game.winner
    practice_loser = practice_game.loser
    print(f"Player {practice_winner.number} won practice game after {practice_game.roll_count} rolls with score {practice_winner.score}.")
    print(f"Player {practice_loser.number} lost practice game after {practice_game.roll_count} rolls with score {practice_loser.score}.")
    print(f"Losing practice score multiplied by rolls:  {practice_loser.score * practice_game.roll_count}")

    real_game = QuantumGame(10, 3, 21, player_positions)
    while real_game.in_progress:
        real_game.take_turn()
    for player_number, wins in real_game.wins_per_player.items():
        print(f"Player {player_number} won {wins} games.")
