#! /usr/bin/env python3

from functools import cmp_to_key


def is_ordered_values(v1, v2):
    """Check if values are in correct order.

    Returns True, False, or None. None indicates that a
    decision could not be make and the next token in the
    packet must be checked.
    """

    if isinstance(v1, int) and isinstance(v2, int):
        if v1 < v2:
            return True
        elif v1 > v2:
            return False
    elif isinstance(v1, list) and isinstance(v2, list):
        for a, b in zip(v1, v2):
            if is_ordered_values(a, b) is not None:
                return is_ordered_values(a, b)

        return is_ordered_values(len(v1), len(v2))
    elif isinstance(v1, list) and isinstance(v2, int):
        return is_ordered_values(v1, [v2])
    elif isinstance(v1, int) and isinstance(v2, list):
        return is_ordered_values([v1], v2)

    return None


def is_ordered_packets(left_packet, right_packet):
    """Determine if two packets are in the correct order."""

    are_ordered = None
    for v1, v2 in zip(left_packet, right_packet):
        correct = is_ordered_values(v1, v2)
        if correct is None:
            continue

        are_ordered = correct
        break

    # if correct ordering could not be determine,
    # check the length of the two packets
    if are_ordered is None:
        are_ordered = is_ordered_values(len(left_packet), len(right_packet))

    return are_ordered


def part1(input_file: str) -> int:
    """Determine sum of packet indices in correct order."""

    packets = open(input_file).read().strip()
    pairs = packets.split('\n\n')

    correct_idx = []
    for idx, pair in enumerate(pairs):
        left, right = pair.split('\n')

        left = eval(left)
        right = eval(right)

        if is_ordered_packets(left, right):
            correct_idx.append(idx+1)

    return sum(correct_idx)


def packet_cmp(left_packet, right_packet):
    """Custom comparator for packets."""

    is_ordered = is_ordered_packets(left_packet, right_packet)

    if is_ordered:
        return -1
    else:
        return 1


def part2(input_file: str) -> int:
    """Determine decoder key for the distress signal."""

    DIVIDER1 = [[2]]
    DIVIDER2 = [[6]]

    packets = [DIVIDER1, DIVIDER2]
    with open(input_file) as f:
        for line in f:
            if line.strip():
                packets.append(eval(line))

    packets = sorted(packets, key=cmp_to_key(packet_cmp))

    return (packets.index(DIVIDER1) + 1) * (packets.index(DIVIDER2) + 1)


if __name__ == '__main__':
    assert part1('test.dat') == 13
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 140
    print(f'Part 2: {part2("input.dat")}')
