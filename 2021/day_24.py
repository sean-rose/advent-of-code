#!/usr/bin/env python

from pathlib import Path
from typing import Optional


FILE_PATH = Path(__file__)


class Instruction:
    def __init__(self, name:str, a: str, b: str = None) -> None:
        self.name = name
        self.a = a
        self.b = b
        if b and b not in ('w', 'x', 'y', 'z'):
            self.b = int(b)


class ALU:
    def __init__(self, vars: Optional[dict[str, int]] = None) -> None:
        self.vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        if vars:
            self.vars.update(vars)

    def process(self, instructions: list[Instruction], inputs: list[int]) -> None:
        vars = self.vars
        input_index = 0
        for instruction in instructions:
            instruction_name = instruction.name
            if instruction_name == 'inp':
                vars[instruction.a] = inputs[input_index]
                input_index += 1
            else:
                b = vars[instruction.b] if isinstance(instruction.b, str) else instruction.b
                if instruction_name == 'add':
                    vars[instruction.a] += b
                elif instruction_name == 'mul':
                    vars[instruction.a] *= b
                elif instruction_name == 'div':
                    vars[instruction.a] //= b
                elif instruction_name == 'mod':
                    vars[instruction.a] %= b
                elif instruction_name == 'eql':
                    vars[instruction.a] = int(vars[instruction.a] == b)


if __name__ == '__main__':
    with open(FILE_PATH.parent / f'{FILE_PATH.stem}_input.txt') as file:
        instructions = [Instruction(*line.split()) for line in file if line.rstrip()]

    input_instruction_sets: list[list[Instruction]] = []
    for instruction in instructions:
        if instruction.name == 'inp':
            input_instruction_set = []
            input_instruction_sets.append(input_instruction_set)
        input_instruction_set.append(instruction)

    min_max_model_numbers_per_z_value: dict[int, list[int, int]] = {0: [0, 0]}
    for input_number, input_instruction_set in enumerate(input_instruction_sets, start=1):
        new_min_max_model_numbers_per_z_value: dict[int, list[int, int]] = {}
        z_cutoff = 26 ** (len(input_instruction_sets) - input_number)
        for z_value, (min_model_number, max_model_number) in min_max_model_numbers_per_z_value.items():
            new_min_model_number_base = min_model_number * 10
            new_max_model_number_base = max_model_number * 10
            for digit in range(1, 10):
                alu = ALU({'z': z_value})
                alu.process(input_instruction_set, [digit])
                z = alu.vars['z']
                if z >= z_cutoff:
                    continue
                new_min_model_number = new_min_model_number_base + digit
                new_max_model_number = new_max_model_number_base + digit
                existing_min_max_model_numbers = new_min_max_model_numbers_per_z_value.get(z)
                if not existing_min_max_model_numbers:
                    new_min_max_model_numbers_per_z_value[z] = [new_min_model_number, new_max_model_number]
                else:
                    if new_min_model_number < existing_min_max_model_numbers[0]:
                        existing_min_max_model_numbers[0] = new_min_model_number
                    if new_max_model_number > existing_min_max_model_numbers[1]:
                        existing_min_max_model_numbers[1] = new_max_model_number
        min_max_model_numbers_per_z_value = new_min_max_model_numbers_per_z_value
        print(
            f"Possible z values after input {input_number}:  {len(min_max_model_numbers_per_z_value)}"
            f"  (min {min(min_max_model_numbers_per_z_value)}, max {max(min_max_model_numbers_per_z_value)})"
        )
    print(f"Min model number:  {min_max_model_numbers_per_z_value[0][0]}")
    print(f"Max model number:  {min_max_model_numbers_per_z_value[0][1]}")
