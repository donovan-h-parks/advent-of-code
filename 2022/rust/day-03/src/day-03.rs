use std::{collections::HashMap, fs};

use itertools::Itertools;

fn part1(data: &str) -> u32 {
    let priority: HashMap<char, u8> = ('a'..='z')
        .chain('A'..='Z')
        .into_iter()
        .enumerate()
        .map(|(idx, ch)| (ch, idx as u8 + 1))
        .collect();

    data.lines()
        .map(|line| {
            let mid_pt = line.len() / 2;
            let compartment1 = &line[0..mid_pt];
            let compartment2 = &line[mid_pt..];

            let common_char = compartment1
                .chars()
                .find(|ch| compartment2.contains(*ch))
                .unwrap();

            *priority.get(&common_char).unwrap() as u32
        })
        .sum::<u32>()
}

fn part2(data: &str) -> u32 {
    let priority: HashMap<char, u8> = ('a'..='z')
        .chain('A'..='Z')
        .into_iter()
        .enumerate()
        .map(|(idx, ch)| (ch, idx as u8 + 1))
        .collect();

    let mut total_priority = 0;
    for mut group in &data.lines().chunks(3) {
        let elf1 = group.next().unwrap();
        let elf2 = group.next().unwrap();
        let elf3 = group.next().unwrap();

        let common_char = elf1
            .chars()
            .find(|ch| elf2.contains(*ch) && elf3.contains(*ch))
            .unwrap();

        total_priority += *priority.get(&common_char).unwrap() as u32;
    }

    total_priority
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
        assert_eq!(results, 157)
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, 70)
    }
}
