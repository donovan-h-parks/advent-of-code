use std::collections::HashSet;

use anyhow::Result;

struct Card {
    winning_numbers: HashSet<u8>,
    card_numbers: HashSet<u8>,
}

impl Card {
    fn score(&self) -> u64 {
        let num_matches = self
            .winning_numbers
            .intersection(&self.card_numbers)
            .count();

        if num_matches == 0 {
            return 0;
        }

        2_u64.pow(num_matches as u32 - 1)
    }
}

fn main() -> Result<()> {
    let input = include_str!("./input.txt");
    let answer = process(input)?;
    println!("answer: {answer}");

    Ok(())
}

pub fn process(input: &str) -> Result<String> {
    let mut answer: u64 = 0;

    for card_data in input.lines() {
        let (_card_name, numbers) = card_data.split_once(':').expect("Valid card data");
        let (winning_numbers, card_numbers) = numbers.split_once('|').expect("Valid number data");

        let winning_numbers: HashSet<u8> = winning_numbers
            .trim()
            .split(' ')
            .filter(|num| !num.is_empty())
            .map(|ch| ch.parse::<u8>().expect("Valid number"))
            .collect();

        let card_numbers: HashSet<u8> = card_numbers
            .trim()
            .split(' ')
            .filter(|num| !num.is_empty())
            .map(|ch| ch.parse::<u8>().expect("Valid number"))
            .collect();

        let card = Card {
            winning_numbers,
            card_numbers,
        };

        answer += card.score();
    }

    Ok(answer.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_answer() {
        let input = include_str!("./test.txt");
        let answer = process(input).unwrap();
        assert_eq!(answer, "13");
    }
}
