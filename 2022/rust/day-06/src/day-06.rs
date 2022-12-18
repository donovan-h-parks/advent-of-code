use std::{collections::HashSet, fs};

fn part1(data: &str) -> usize {
    const START_OF_PACKET_SIZE: usize = 4;

    let packet_idx = data
        .as_bytes()
        .windows(START_OF_PACKET_SIZE)
        .position(|window| {
            let unique_chars: HashSet<&u8> = HashSet::from_iter(window.iter());
            unique_chars.len() == window.len()
        })
        .unwrap();

    packet_idx + START_OF_PACKET_SIZE
}

fn part2(data: &str) -> usize {
    const START_OF_MESSAGE_SIZE: usize = 14;

    let message_idx = data
        .as_bytes()
        .windows(START_OF_MESSAGE_SIZE)
        .position(|window| {
            let unique_chars: HashSet<&u8> = HashSet::from_iter(window.iter());
            unique_chars.len() == window.len()
        })
        .unwrap();

    message_idx + START_OF_MESSAGE_SIZE
}

fn main() {
    let data = fs::read_to_string("./input.dat").unwrap();

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
        assert_eq!(results, 7)
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, 19)
    }
}
