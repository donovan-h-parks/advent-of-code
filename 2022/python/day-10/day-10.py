#! /usr/bin/env python3

from typing import List

CPU_CYCLES = {'noop': 1, 'addx': 2}

SPRITE_WIDTH = 3
CRT_WIDTH = 40
CRT_HEIGHT = 6

LIGHT_CHAR = '#'
DARK_CHAR = '.'


def part1(input_file: str) -> int:
    """Determine sum of signal strength for program execution."""

    cycle = 0
    registerX = 1
    signal_strength = 0
    with open(input_file) as f:
        for line in f:
            tokens = line.strip().split()
            instruction = tokens[0]

            # increment clock cycle for instruction and track
            # sum signal strength at 20, 60, 100, 140, ...
            for _ in range(CPU_CYCLES[instruction]):
                cycle += 1
                if (cycle - 20) % 40 == 0:
                    signal_strength += cycle*registerX

            # modify register at end of instruction cycles
            if instruction == 'addx':
                registerX += int(tokens[1])

    return signal_strength


def part2(input_file: str) -> List[str]:
    """Determine contents of CRT display after program execution."""

    # setup blank CRT display
    display = [['-']*CRT_WIDTH for _ in range(CRT_HEIGHT)]

    # process instructions and set CRT pixels
    cycle = 0
    registerX = 1
    with open(input_file) as f:
        for line in f:
            tokens = line.strip().split()
            instruction = tokens[0]

            # increment clock cycle for instruction and track
            # sum signal strength at 20, 60, 100, 140, ...
            for _ in range(CPU_CYCLES[instruction]):
                col = cycle % CRT_WIDTH
                row = cycle//CRT_WIDTH

                if abs(registerX - col) <= 1:
                    display[row][col] = '#'
                else:
                    display[row][col] = '.'

                cycle += 1

            # modify register at end of instruction cycles
            if instruction == 'addx':
                registerX += int(tokens[1])

    # print contents of display
    display = [''.join(row) for row in display]

    return display


if __name__ == '__main__':
    assert part1('test.dat') == 13140
    print(f'Part 1: {part1("input.dat")}')

    TEST_DISPLAY = [
        '##..##..##..##..##..##..##..##..##..##..',
        '###...###...###...###...###...###...###.',
        '####....####....####....####....####....',
        '#####.....#####.....#####.....#####.....',
        '######......######......######......####',
        '#######.......#######.......#######.....']
    assert part2('test.dat') == TEST_DISPLAY

    print('Part 2:')
    display = part2('input.dat')
    for row in display:
        print(row)
