#! /usr/bin/env python3

import re
from collections import deque
from typing import List


def initialize_stacks(initial_state: List[str]) -> List[deque]:
    """Initialize stacks.

    Example stack initialization:
        [D]
    [N] [C]
    [Z] [M] [P]
    1   2   3
    """

    # read position of boxes in each stack along the input lines
    stack_ids = initial_state[-1]

    stack_idx = []
    for idx, ch in enumerate(stack_ids):
        if ch.isnumeric():
            stack_idx.append(idx)

    # initialize empty stacks
    stacks = [deque() for _ in range(len(stack_idx))]

    # add crates to the stack starting at the top
    # and moving to the bottom
    for line in initial_state[:-1]:
        for stack_num, idx in enumerate(stack_idx):
            if idx >= len(line):
                continue

            if line[idx].isalpha():
                stacks[stack_num].append(line[idx])

    return stacks


def execute_procedure(line: str, stacks: List[deque]):
    """Update stacks by executing rearrangement procedure.

    Example procedure: move 3 from 1 to 3
      Move 3 crates from stack 1 to stack 3 one at a time.
    """

    procedure = [int(n) for n in re.findall(r'\d+', line)]
    steps, source_stack, dest_stack = procedure

    # execute procedure taking into account zero-based indexing
    for _ in range(steps):
        crate = stacks[source_stack-1].popleft()
        stacks[dest_stack-1].appendleft(crate)


def part1(input_file: str) -> str:
    """Determine top crates in each stack after rearrangement procedure."""

    # initialize stacks and parse rearrangement procuedure
    with open(input_file) as f:
        # read initial state of stacks
        initial_state = []
        for line in f:
            if not line.strip():
                break

            initial_state.append(line)

        # setup stacks
        stacks = initialize_stacks(initial_state)

        # execute rearrangement procedure
        for line in f:
            execute_procedure(line, stacks)

    # read name of boxes on crate of each stack
    top_crates = ''.join([stack.popleft() for stack in stacks])

    return top_crates


def execute_crate_mover_9001(line: str, stacks: List[deque]):
    """Update stacks by executing CrateMover 9001 rearrangement procedure.

    Example procedure: move 3 from 1 to 3
      Move 3 crates together from stack 1 to stack 3.
    """

    procedure = [int(n) for n in re.findall(r'\d+', line)]
    steps, source_stack, dest_stack = procedure

    # execute procedure taking into account zero-based indexing. Crates to
    # move are pushed onto a queue in reverse order since extending a deque
    # will reverse the order back.
    crates_to_move = deque()
    for _ in range(steps):
        crates_to_move.appendleft(stacks[source_stack-1].popleft())

    stacks[dest_stack-1].extendleft(crates_to_move)


def part2(input_file: str) -> str:
    """Determine top crates in each stack after rearrangement procedure using CrateMover 9001."""

    # initialize stacks and parse rearrangement procuedure
    with open(input_file) as f:
        # read initial state of stacks
        initial_state = []
        for line in f:
            if not line.strip():
                break

            initial_state.append(line)

        # setup stacks
        stacks = initialize_stacks(initial_state)

        # execute rearrangement procedure
        for line in f:
            execute_crate_mover_9001(line, stacks)

    # read name of boxes on crate of each stack
    top_crates = ''.join([stack.popleft() for stack in stacks])

    return top_crates


if __name__ == '__main__':
    assert part1('test.dat') == 'CMZ'
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 'MCD'
    print(f'Part 2: {part2("input.dat")}')
