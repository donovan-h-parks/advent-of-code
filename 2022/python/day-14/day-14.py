#! /usr/bin/env python3

import math


START_X = 500
AIR = '.'
SAND = '0'
ROCK = '#'


def part1(input_file: str) -> int:
    """Determine number of units of sand that come to rest."""

    # read rock structures and bounds of rock formation
    x_min = 1e6
    x_max = 0
    y_max = 0

    rock_paths = []
    with open(input_file) as f:
        for line in f:
            path = [list(map(int, pt.split(',')))
                    for pt in line.strip().split(' -> ')]

            rock_paths.append(path)

            for p in path:
                x_min = min(x_min, p[0])
                x_max = max(x_max, p[0])
                y_max = max(y_max, p[1])

    # setup empty grid
    width = x_max-x_min+1
    height = y_max+1

    grid = [[AIR]*width for _ in range(height)]

    # fill in rock structures
    for path in rock_paths:
        prev_x = path[0][0]
        prev_y = path[0][1]
        for x, y in path[1:]:
            dx = x - prev_x
            dy = y - prev_y

            if dx != 0:
                sign = math.copysign(1, dx)
                for offset in range(abs(dx)+1):
                    grid[y][prev_x+int(sign*offset) - x_min] = ROCK
            else:
                sign = math.copysign(1, dy)
                for offset in range(abs(dy)+1):
                    grid[prev_y+int(sign*offset)][x - x_min] = ROCK

            prev_x = x
            prev_y = y

    # fill in sand
    num_sand = 0
    while True:
        sand_x = START_X - x_min

        for y in range(0, height):
            if grid[y][sand_x] != AIR:
                if grid[y][sand_x-1] == AIR:
                    sand_x -= 1
                elif grid[y][sand_x+1] == AIR:
                    sand_x += 1
                else:
                    num_sand += 1
                    grid[y-1][sand_x] = SAND
                    break

        if sand_x < 0 or sand_x > width:
            break

    return num_sand


def part2(input_file: str) -> int:
    """Determine number of units of sand that come to rest with an infinite floor."""

    # setup floor and "cheat" the infinite extent as 500 units to the left or right
    # of the origin of the sand
    FLOOR_Y_OFFSET = 2
    FLOOR_X_MIN = 0
    FLOOR_X_MAX = 1000

    # read rock structures and lowest rock formation
    y_max = 0

    rock_paths = []
    with open(input_file) as f:
        for line in f:
            path = [list(map(int, pt.split(',')))
                    for pt in line.strip().split(' -> ')]

            rock_paths.append(path)

            for p in path:
                y_max = max(y_max, p[1])

    # setup empty grid
    width = FLOOR_X_MAX - FLOOR_X_MIN + 1
    height = y_max + FLOOR_Y_OFFSET + 1

    grid = [[AIR]*width for _ in range(height)]

    # fill in rock structures
    for path in rock_paths:
        prev_x = path[0][0]
        prev_y = path[0][1]
        for x, y in path[1:]:
            dx = x - prev_x
            dy = y - prev_y

            if dx != 0:
                sign = math.copysign(1, dx)
                for offset in range(abs(dx)+1):
                    grid[y][prev_x+int(sign*offset)] = ROCK
            else:
                sign = math.copysign(1, dy)
                for offset in range(abs(dy)+1):
                    grid[prev_y+int(sign*offset)][x] = ROCK

            prev_x = x
            prev_y = y

    # fill in floor below lowest rock formation
    grid[height-2] = [AIR]*width
    grid[height-1] = [ROCK]*width

    # fill in sand
    num_sand = 0
    while True:
        sand_x = START_X

        for y in range(0, height):
            if grid[y][sand_x] != AIR:
                if grid[y][sand_x-1] == AIR:
                    sand_x -= 1
                elif grid[y][sand_x+1] == AIR:
                    sand_x += 1
                else:
                    num_sand += 1
                    grid[y-1][sand_x] = SAND
                    break

        # check if sand was placed at the sand origin
        if grid[0][START_X] == SAND:
            break

    return num_sand


if __name__ == '__main__':
    assert part1('test.dat') == 24
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 93
    print(f'Part 2: {part2("input.dat")}')
