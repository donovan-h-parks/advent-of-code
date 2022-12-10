#! /usr/bin/env python3

from collections import defaultdict


def part1(input_file: str) -> int:
    """Determine total size of all directories under 100000."""

    path_to_cwd = []
    dir_sizes = defaultdict(int)
    with open(input_file) as f:
        for line in f:
            tokens = line.strip().split(' ')

            # process change directory commands and keep
            # track of position in directory tree
            if tokens[0] == '$' and tokens[1] == 'cd':
                    if tokens[2] == '/':
                        path_to_cwd = ['']
                    elif tokens[2] == '..':
                        path_to_cwd.pop()
                    else:
                        path_to_cwd.append(tokens[2])
            else:
                # add size of files to current directory and all parent directories
                if tokens[0].isnumeric():
                    for idx in range(len(path_to_cwd)):
                        cur_dir = '/' + '/'.join(path_to_cwd[1:idx+1])
                        dir_sizes[cur_dir] += int(tokens[0])

    # get total size of all directories under 100000
    total_size = sum([size for size in dir_sizes.values() if size <= 100000])

    return total_size


def part2(input_file: str) -> int:
    """Determine size of smallest directory to delete to reach required free space."""

    DISK_SIZE = 70000000
    REQUIRED_FREE_SIZE = 30000000

    # get size of all directories
    path_to_cwd = []
    dir_sizes = defaultdict(int)
    with open(input_file) as f:
        for line in f:
            tokens = line.strip().split(' ')

            # process change directory commands and keep
            # track of position in directory tree
            if tokens[0] == '$' and tokens[1] == 'cd':
                    if tokens[2] == '/':
                        path_to_cwd = ['']
                    elif tokens[2] == '..':
                        path_to_cwd.pop()
                    else:
                        path_to_cwd.append(tokens[2])
            else:
                # add size of files to current directory and all parent directories
                if tokens[0].isnumeric():
                    for idx in range(len(path_to_cwd)):
                        cur_dir = '/' + '/'.join(path_to_cwd[1:idx+1])
                        dir_sizes[cur_dir] += int(tokens[0])

    # find directories resulting in enough free disk space
    cur_free = DISK_SIZE - dir_sizes['/']

    smallest_dir = DISK_SIZE
    for cur_size in dir_sizes.values():
        if cur_free + cur_size >= REQUIRED_FREE_SIZE and cur_size < smallest_dir:
            smallest_dir = cur_size

    return smallest_dir


if __name__ == '__main__':
    assert part1('test.dat') == 95437
    print(f'Part 1: {part1("input.dat")}')

    assert part2('test.dat') == 24933642
    print(f'Part 2: {part2("input.dat")}')
