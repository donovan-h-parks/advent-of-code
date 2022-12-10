#! /usr/bin/env python3

from typing import Iterable


def part1(input_file: str) -> int:
    """Determine largest number of calories carried by an Elf."""

    max_calories = 0
    cur_calories = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            if line:
                cur_calories += int(line)
            else:
                # empty line signifies that start of a new elf
                max_calories = max(cur_calories, max_calories)
                cur_calories = 0

    return max_calories


def part2(input_file: str) -> int:
    """Determine number of calories carried by top three Elves."""

    calories = []
    cur_calories = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            if line:
                cur_calories += int(line)
            else:
                # empty line signifies that start of a new elf
                calories.append(cur_calories)
                cur_calories = 0

    calories.append(cur_calories)

    return sum(sorted(calories, reverse=True)[0:3])


if __name__ == '__main__':
    assert part1('test.dat') == 24000
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 45000
    print(f'Part 2: {part2("input.dat")}')
