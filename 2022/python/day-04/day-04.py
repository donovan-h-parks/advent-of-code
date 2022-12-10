#! /usr/bin/env python3


def is_fully_contained(start1: int, end1: int, start2: int, end2: int) -> bool:
    """Check if interval 1 is fully contained in interval 2."""

    return start1 >= start2 and end1 <= end2


def is_overlap(start1: int, end1: int, start2: int, end2: int) -> bool:
    """Check if interval 1 and interval 2 overlap."""

    return start2 <= start1 <= end2 or start1 <= start2 <= end1


def part1(input_file: str) -> int:
    """Find number of fully contained sections across assignment pairs."""

    num_contained = 0
    with open(input_file) as f:
        for line in f:
            assignments = line.strip().split(',')
            assert len(assignments) == 2

            start1, end1 = map(int, assignments[0].split('-'))
            start2, end2 = map(int, assignments[1].split('-'))

            if is_fully_contained(start1, end1, start2, end2):
                num_contained += 1
            elif is_fully_contained(start2, end2, start1, end1):
                num_contained += 1

    return num_contained


def part2(input_file: str) -> int:
    """Determine number of overlapping assignment pairs."""

    num_overlap = 0
    with open(input_file) as f:
        for line in f:
            assignments = line.strip().split(',')
            assert len(assignments) == 2

            start1, end1 = map(int, assignments[0].split('-'))
            start2, end2 = map(int, assignments[1].split('-'))

            if is_overlap(start1, end1, start2, end2):
                num_overlap += 1

    return num_overlap


if __name__ == '__main__':
    assert part1('test.dat') == 2
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 4
    print(f'Part 2: {part2("input.dat")}')
