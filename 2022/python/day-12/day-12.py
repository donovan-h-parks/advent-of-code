#! /usr/bin/env python3

from typing import List
from collections import deque
from dataclasses import dataclass


START = 'S'
END = 'E'


@dataclass
class Node:
    x: int
    y: int
    num_steps: int


def get_height(node: Node, height_map: List[str]):
    """Get height at given position in map."""

    if height_map[node.y][node.x] == START:
        return 1
    elif height_map[node.y][node.x] == END:
        return 26

    return ord(height_map[node.y][node.x]) - ord('a') + 1


def breadth_first_search(node: Node, height_map: List[str]) -> Node:
    """Perform breadth first search to destination."""

    width = len(height_map[0])
    height = len(height_map)

    stack = deque([node])
    visited = set([(node.x, node.y)])
    while stack:
        cur_node = stack.popleft()

        if height_map[cur_node.y][cur_node.x] == END:
            return cur_node

        cur_height = get_height(cur_node, height_map)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x = cur_node.x - dx
            y = cur_node.y - dy
            dest_node = Node(x, y, cur_node.num_steps+1)

            if 0 <= x < width and 0 <= y < height and (x, y) not in visited:
                dest_height = get_height(dest_node, height_map)
                if dest_height <= cur_height + 1:
                    stack.append(dest_node)
                    visited.add((x, y))


def part1(input_file: str) -> int:
    """Determine shorted path to destination."""

    # read the height map and find starting location
    height_map = []
    start = None
    with open(input_file) as f:
        row = 0
        for line in f:
            data = line.strip()
            height_map.append(data)

            if START in data:
                start = Node(data.index(START), row, 0)

            row += 1

    assert start is not None

    # perform depth-first search to end node
    node = breadth_first_search(start, height_map)

    return node.num_steps


def part2(input_file: str) -> int:
    """Determine shortest path to destination starting from any position with an elevation of a."""

    # read the height map and find starting locations
    height_map = []
    starts = []
    with open(input_file) as f:
        row = 0
        for line in f:
            data = line.strip()
            height_map.append(data)

            if START in data:
                starts.append(Node(data.index(START), row, 0))
            elif 'a' in data:
                starts.append(Node(data.index('a'), row, 0))

            row += 1

    # perform depth-first search to end node for each possible start
    min_steps = min([breadth_first_search(start, height_map).num_steps
                    for start in starts])

    return min_steps


if __name__ == '__main__':
    assert part1('test.dat') == 31
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 29
    print(f'Part 2: {part2("input.dat")}')
