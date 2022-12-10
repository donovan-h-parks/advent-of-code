#! /usr/bin/env python3


def update_tail_pos(head_pos, tail_pos):
    """Update position of tail based on the head position."""

    dx = head_pos[0] - tail_pos[0]
    dy = head_pos[1] - tail_pos[1]

    if dx == 0 and abs(dy) > 1:
        #  tail needs to move along row
        tail_pos[1] += 1 if dy > 0 else -1
    elif abs(dx) > 1 and dy == 0:
        #  tail needs  to move along columns
        tail_pos[0] += 1 if dx > 0 else -1
    elif abs(dx) >= 2 or abs(dy) >= 2:
        # tail needs to move on diagonal to catch up to tail
        tail_pos[0] += 1 if dx > 0 else -1
        tail_pos[1] += 1 if dy > 0 else -1

    assert abs(head_pos[0] - tail_pos[0]) <= 1
    assert abs(head_pos[1] - tail_pos[1]) <= 1

    return tail_pos


def part1(input_file: str) -> int:
    """Determine number of positions tail of rope visits at least once."""

    # read in motions for the head of rope
    motions = []
    with open(input_file) as f:
        for line in f:
            direct, steps = line.strip().split()
            motions.append((direct, int(steps)))

    # run through motions updating the position of the
    # head and tail; keep track of each position the tail
    # occupies
    head_pos = [0, 0]
    tail_pos = [0, 0]
    tail_occupied = set([(0, 0)])

    for motion in motions:
        direct, steps = motion

        for _ in range(steps):
            if direct == 'R':
                head_pos = (head_pos[0]+1, head_pos[1])
            elif direct == 'L':
                head_pos = (head_pos[0]-1, head_pos[1])
            elif direct == 'U':
                head_pos = (head_pos[0], head_pos[1]+1)
            elif direct == 'D':
                head_pos = (head_pos[0], head_pos[1]-1)

            tail_pos = update_tail_pos(head_pos, tail_pos)
            tail_occupied.add(tuple(tail_pos))

    return len(tail_occupied)


def part2(input_file: str) -> int:
    """Determine number of positions knot 9 of rope visits at least once."""

    # read in motions for the head of rope
    motions = []
    with open(input_file) as f:
        for line in f:
            direct, steps = line.strip().split()
            motions.append((direct, int(steps)))

    # run through motions updating the position of the
    # head and tail; keep track of each position the tail
    # occupies
    head_pos = [0, 0]
    tail_pos = [[0, 0] for _ in range(9)]
    knot9_occupied = set([(0, 0)])

    for motion in motions:
        direct, steps = motion

        for _ in range(steps):
            if direct == 'R':
                head_pos = (head_pos[0]+1, head_pos[1])
            elif direct == 'L':
                head_pos = (head_pos[0]-1, head_pos[1])
            elif direct == 'U':
                head_pos = (head_pos[0], head_pos[1]+1)
            elif direct == 'D':
                head_pos = (head_pos[0], head_pos[1]-1)

            tail_pos[0] = update_tail_pos(head_pos, tail_pos[0])

            for idx in range(1, 9):
                tail_pos[idx] = update_tail_pos(tail_pos[idx-1], tail_pos[idx])

            knot9_occupied.add(tuple(tail_pos[-1]))

    return len(knot9_occupied)


if __name__ == '__main__':
    assert part1('test.dat') == 13
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test2.dat') == 36
    print(f'Part 2: {part2("input.dat")}')
