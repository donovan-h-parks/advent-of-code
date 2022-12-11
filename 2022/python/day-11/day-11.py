#! /usr/bin/env python3

from __future__ import annotations
from typing import List


class Monkey:
    """Monkey playing keep away."""

    def __init__(self, monkey_def: List[str]) -> None:
        """Initialize monkey from text definition."""

        self.name = monkey_def[0].replace(':', '')

        # list of items held by monkey; the value of the item
        # is it's worry level
        self.items = [int(item)
                      for item in monkey_def[1].rsplit(':')[-1].split(',')]

        self.operation = eval(
            f'lambda old: {monkey_def[2].split("=")[-1].strip()}')

        self.divisor = int(monkey_def[3].split()[-1])
        self.is_div_target = int(monkey_def[4].split()[-1])
        self.not_div_target = int(monkey_def[5].split()[-1])

        self.items_inspected = 0

    def __str__(self):
        """Print out monkey properties."""

        s = f'Name: {self.name}\n'
        s += f'Items: {self.items}\n'
        s += f'Operation: {self.operation}\n'
        s += f'Divisor: {self.divisor}\n'
        s += f'Divisible target: {self.is_div_target}\n'
        s += f'Not divisible target: {self.not_div_target}'

        return s

    def take_turn_part1(self, monkeys: List[Monkey]) -> None:
        """Take turn in game of keep away using part 1 rules."""

        # inspect each item in turn and determine monkey to pass item to
        for item in self.items:
            self.items_inspected += 1

            new_worry_level = self.operation(item) // 3

            if new_worry_level % self.divisor == 0:
                monkeys[self.is_div_target].items.append(new_worry_level)
            else:
                monkeys[self.not_div_target].items.append(new_worry_level)

        self.items = []

    def take_turn_part2(self, monkeys: List[Monkey], modulo: int) -> None:
        """Take turn in game of keep away using part 2 rules."""

        # inspect each item in turn and determine monkey to pass item to
        for item in self.items:
            self.items_inspected += 1

            new_worry_level = self.operation(item) % modulo

            if new_worry_level % self.divisor == 0:
                monkeys[self.is_div_target].items.append(new_worry_level)
            else:
                monkeys[self.not_div_target].items.append(new_worry_level)

        self.items = []


def initialize_monkeys(input_file: str) -> List[Monkey]:
    """Initialize monkeys from descriptions in file."""

    monkeys = []
    with open(input_file) as f:
        monkey_def = []
        for line in f:
            if line.strip():
                monkey_def.append(line.strip())
            else:
                monkeys.append(Monkey(monkey_def))
                monkey_def = []

    monkeys.append(Monkey(monkey_def))

    return monkeys


def part1(input_file: str) -> int:
    """Determine two most active monkeys and their level of `monkey business`."""

    NUM_ROUNDS = 20

    monkeys = initialize_monkeys(input_file)

    # play rounds of keep away; each round consists of each
    # monkey inspecting all items it has and throwing the item
    # to a different monkey based on its behaviour
    for _ in range(NUM_ROUNDS):
        for monkey in monkeys:
            monkey.take_turn_part1(monkeys)

    # determine 'monkey business' which is the product of the
    # numer of items inspected by the two monkeys which has
    # inspected the most items
    num_inspected = [monkey.items_inspected for monkey in monkeys]
    num_inspected.sort(reverse=True)

    return num_inspected[0] * num_inspected[1]


def part2(input_file: str) -> List[str]:
    """Determine two most active monkeys and their level of `monkey business`.

    This is challenging since the worry level of items can become extremely
    large. Python can handle large integers, but operations becoming excessively
    slow. In many languages this would result in an overflow. The solution to this
    is to note that the test performed by each monkey to determine which monkey an
    item should be passed to is a divisibility test. As such, the worry level of
    and item can be stored as the modulo M, where M is the product across all the
    divisors of the divisibility tests being performed. Complicated, and I had to
    look this up!
    """

    NUM_ROUNDS = 10000

    monkeys = initialize_monkeys(input_file)

    # determine product of modulo operations performed
    # across all monkeys; this is used to stop the worry
    # level of the monkeys from becoming extremely large
    modulo_factor = 1
    for m in monkeys:
        modulo_factor *= m.divisor

    # play rounds of keep away; each round consists of each
    # monkey inspecting all items it has and throwing the item
    # to a different monkey based on its behaviour
    for _ in range(NUM_ROUNDS):
        for monkey in monkeys:
            monkey.take_turn_part2(monkeys, modulo_factor)

    # determine 'monkey business' which is the product of the
    # numer of items inspected by the two monkeys which has
    # inspected the most items
    num_inspected = [monkey.items_inspected for monkey in monkeys]
    num_inspected.sort(reverse=True)

    return num_inspected[0] * num_inspected[1]


if __name__ == '__main__':
    assert part1('test.dat') == 10605
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 2713310158
    print(f'Part 2: {part2("input.dat")}')
