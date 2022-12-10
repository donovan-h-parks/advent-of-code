#! /usr/bin/env python3


def marker_index(transmission: str, num_identical_chars: int) -> int:
    """Find index after specified number of identical characters."""

    for idx in range(len(transmission)):
        if len(set(transmission[idx:idx+num_identical_chars])) == num_identical_chars:
            return idx+num_identical_chars

    return -1


def part1(input_file: str) -> int:
    """Determine index after start-of-packet marker or -1 if no marker is found."""

    MARKER_LEN = 4
    transmission = open(input_file).readline()
    return marker_index(transmission, MARKER_LEN)


def part2(input_file: str) -> int:
    """Determine index after start-of-message marker or -1 if no marker is found."""

    MARKER_LEN = 14
    transmission = open(input_file).readline()
    return marker_index(transmission, MARKER_LEN)


if __name__ == '__main__':
    assert part1('test.dat') == 7
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 19
    print(f'Part 2: {part2("input.dat")}')
