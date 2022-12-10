#! /usr/bin/env python3

import math


def part1(input_file: str) -> int:
    """Determine number of visible trees."""

    # read tree grid into a list of lists
    trees = []
    with open(input_file) as f:
        for line in f:
            tree_row = line.strip()
            trees.append(list(map(int, tree_row)))

    # search along each row and column and mark visible trees
    visible = [[0]*len(trees[0]) for _ in range(len(trees))]

    # visible from the right
    for row_idx, tree_row in enumerate(trees):
        largest_tree = -1
        for col_idx, height in enumerate(tree_row):
            if height > largest_tree:
                visible[row_idx][col_idx] = 1
                largest_tree = height

    # visible from the left
    for row_idx, tree_row in enumerate(trees):
        largest_tree = -1
        for col_idx, height in reversed(list(enumerate(tree_row))):
            if height > largest_tree:
                visible[row_idx][col_idx] = 1
                largest_tree = height

    # visible from the top
    for col_idx in range(len(trees[0])):
        largest_tree = -1
        for row_idx in range(len(trees)):
            height = trees[row_idx][col_idx]
            if height > largest_tree:
                visible[row_idx][col_idx] = 1
                largest_tree = height

    # visible from the bottom
    for col_idx in range(len(trees[0])):
        largest_tree = -1
        for row_idx in reversed(range(len(trees))):
            height = trees[row_idx][col_idx]
            if height > largest_tree:
                visible[row_idx][col_idx] = 1
                largest_tree = height

    # determine total number of visible trees
    visible_trees = sum([sum(v) for v in visible])

    return visible_trees


def part2(input_file: str) -> int:
    """Determine highest scenic score."""

    # read tree grid into a list of lists
    trees = []
    with open(input_file) as f:
        for line in f:
            tree_row = line.strip()
            trees.append(list(map(int, tree_row)))

    # calculate scenic score for each tree
    scenic_scores = [[0]*len(trees[0]) for _ in range(len(trees))]

    num_rows = len(trees)
    num_cols = len(trees[0])

    for cur_row_idx in range(1, num_rows-1):
        for cur_col_idx in range(1, num_cols-1):
            cur_tree_height = trees[cur_row_idx][cur_col_idx]
            cur_scores = []

            # look left
            score = 0
            for col_idx in reversed(range(0, cur_col_idx)):
                score += 1
                if trees[cur_row_idx][col_idx] >= cur_tree_height:
                    break

            cur_scores.append(score)

            # look right
            score = 0
            for col_idx in range(cur_col_idx+1, num_cols):
                score += 1
                if trees[cur_row_idx][col_idx] >= cur_tree_height:
                    break

            cur_scores.append(score)

            # look up
            score = 0
            for row_idx in reversed(range(0, cur_row_idx)):
                score += 1
                if trees[row_idx][cur_col_idx] >= cur_tree_height:
                    break

            cur_scores.append(score)

            # look down
            score = 0
            for row_idx in range(cur_row_idx+1, num_rows):
                score += 1
                if trees[row_idx][cur_col_idx] >= cur_tree_height:
                    break

            cur_scores.append(score)

            scenic_scores[cur_row_idx][cur_col_idx] = math.prod(cur_scores)

    highest_score = max([max(r) for r in scenic_scores])

    return highest_score


if __name__ == '__main__':
    assert part1('test.dat') == 21
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 8
    print(f'Part 2: {part2("input.dat")}')
