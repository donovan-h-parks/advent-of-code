#! /usr/bin/env python3

from typing import Iterable


def find_common_item(items: Iterable[Iterable]) -> str:
    """Find single item that is common across all item lists."""

    assert len(items) >= 2

    common = set(items[0]).intersection(*[set(it) for it in items[1:]])
    assert len(common) == 1

    return common.pop()


def item_priority(item: str) -> int:
    """Get priority value of item."""

    assert len(item) == 1

    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    elif 'A' <= item <= 'Z':
        return ord(item) - ord('A') + 27

    raise ValueError('Invalid item value.')


def part1(input_file: str) -> int:
    """Determine total priority of items common between rucksack compartments."""

    priority_common_items = 0
    with open(input_file) as f:
        for line in f:
            line = line.strip()

            # determine items in each of the equally-sized compartments
            middle_idx = len(line)//2
            compartment1 = line[:middle_idx]
            compartment2 = line[middle_idx:]
            assert len(compartment1) == len(compartment2)

            # find single common item between two comparments
            common_item = find_common_item([compartment1, compartment2])

            # add priority of common item
            priority_common_items += item_priority(common_item)

    return priority_common_items


def part2(input_file: str) -> int:
    """Determine total priority of badges in each group of three."""

    priority_badges = 0
    with open(input_file) as f:
        group_sacks = []
        for idx, line in enumerate(f):
            line = line.strip()

            # add items to this group
            group_sacks.append(set(line))

            if len(group_sacks) == 3:
                # find badge (common item) between 3 elves
                common_item = find_common_item(group_sacks)
                priority_badges += item_priority(common_item)
                group_sacks = []

    return priority_badges


if __name__ == '__main__':
    assert part1('test.dat') == 157
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 70
    print(f'Part 2: {part2("input.dat")}')
