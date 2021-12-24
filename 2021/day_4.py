#!/usr/bin/env python

from pathlib import Path


FILE_PATH = Path(__file__)


class BingoNumber:
    def __init__(self, value: int) -> None:
        self.value = value
        self.is_marked = False


class BingoBoard:
    def __init__(self) -> None:
        self.rows: list[list[BingoNumber]] = []
    
    def add_row(self, row: list[BingoNumber]) -> None:
        self.rows.append(row)

    def has_won(self) -> bool:
        return (
            any(all(number.is_marked for number in row) for row in self.rows)
            or any(all(row[column].is_marked for row in self.rows) for column in range(len(self.rows[0])))
        )
    
    def sum_unmarked_numbers(self) -> int:
        return sum(number.value for row in self.rows for number in row if not number.is_marked)


if __name__ == '__main__':
    numbers = {number: BingoNumber(number) for number in range(100)}
    boards: list[BingoBoard] = []

    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        numbers_to_be_drawn = [numbers[int(number_str)] for number_str in file.readline().rstrip().split(',')]
        print(f"Numbers to be drawn:  {len(numbers_to_be_drawn)}")

        new_board = None
        for line in file.readlines():
            new_row = [numbers[int(number_str)] for number_str in line.split()]
            if new_row:
                if not new_board:
                    new_board = BingoBoard()
                    boards.append(new_board)
                new_board.add_row(new_row)
            else:
                new_board = None
        print(f"Boards:  {len(boards)}")
    
    winning_board = None
    for number in numbers_to_be_drawn:
        number.is_marked = True
        for board_number, board in enumerate(boards, start=1):
            if board.has_won():
                winning_board = board
                winning_score = winning_board.sum_unmarked_numbers() * number.value
                print(f"Board {board_number} won with score {winning_score}.")
                break
        if winning_board:
            break
    else:
        raise Exception("Didn't find a winning board.")
