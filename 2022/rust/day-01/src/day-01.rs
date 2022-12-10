use itertools::Itertools;
use std::fs;

/// Determine maximum number of calories carried by an elf.
fn part1(data: &str) -> u32 {
    data.split("\n\n")
        .map(|elf_load| {
            elf_load
                .split_terminator('\n')
                .map(|item| item.parse::<u32>().unwrap())
                .sum()
        })
        .max()
        .unwrap()
}

/// Determine number of calories carried by 3 elves carrying the most calories.
fn part2(data: &str) -> u32 {
    data.split("\n\n")
        .map(|elf_load| {
            elf_load
                .split_terminator('\n')
                .map(|item| item.parse::<u32>().unwrap())
                .sum::<u32>()
        })
        .sorted_by(|a, b| b.cmp(a))
        .take(3)
        .sum()
}

fn main() {
    let data = fs::read_to_string("input.dat").unwrap();

    println!("Part 1: {}", part1(&data));
    println!("Part 2: {}", part2(&data));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part1(&test_data);
        assert_eq!(results, 24000)
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, 45000)
    }
}
