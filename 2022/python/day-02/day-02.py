#! /usr/bin/env python3

from typing import Iterable


def part1(input_file: str) -> int:
    """Calculate score of assumed rock, paper, scissors strategy guide."""

    game_score = {}
    game_score['A X'] = 4
    game_score['A Y'] = 8
    game_score['A Z'] = 3
    game_score['B X'] = 1
    game_score['B Y'] = 5
    game_score['B Z'] = 9
    game_score['C X'] = 7
    game_score['C Y'] = 2
    game_score['C Z'] = 6

    score = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            score += game_score[line]

    return score


def part2(input_file: str) -> int:
    """Calculate score of actual rock, paper, scissors strategy guide."""

    game_score = {}
    game_score['A X'] = 3
    game_score['A Y'] = 4
    game_score['A Z'] = 8
    game_score['B X'] = 1
    game_score['B Y'] = 5
    game_score['B Z'] = 9
    game_score['C X'] = 2
    game_score['C Y'] = 6
    game_score['C Z'] = 7

    score = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            score += game_score[line]

    return score


if __name__ == '__main__':
    assert part1('test.dat') == 15
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 12
    print(f'Part 2: {part2("input.dat")}')
