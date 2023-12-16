use std::collections::HashSet;

use anyhow::Result;

struct Card {
    winning_numbers: HashSet<u8>,
    card_numbers: HashSet<u8>,
}

impl Card {
    fn score(&self) -> usize {
        let num_matches = self
            .winning_numbers
            .intersection(&self.card_numbers)
            .count();

        num_matches
    }
}

fn main() -> Result<()> {
    let input = include_str!("./input.txt");
    let answer = process(input)?;
    println!("answer: {answer}");

    Ok(())
}

pub fn process(input: &str) -> Result<String> {
    let mut cards = Vec::new();
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

        cards.push(card);
    }

    // keep track of how many times a card has been won so we
    // can add that to the following set of cards
    let mut card_counts: Vec<_> = vec![1_u64; cards.len()];
    for (card_idx, card) in cards.iter().enumerate() {
        let cur_count = card_counts[card_idx];

        for card_count in card_counts.iter_mut().skip(card_idx + 1).take(card.score()) {
            *card_count += cur_count;
        }
    }

    let answer: u64 = card_counts.iter().sum();

    Ok(answer.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_answer() {
        let input = include_str!("./test.txt");
        let answer = process(input).unwrap();
        assert_eq!(answer, "30");
    }
}
