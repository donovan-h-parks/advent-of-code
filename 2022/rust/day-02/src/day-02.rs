use std::{fs, str::FromStr};

/// Shapes for the game rock, paper, scissors.
#[derive(Copy, Clone)]
enum Shape {
    Rock,
    Paper,
    Scissors,
}

impl FromStr for Shape {
    type Err = String;
    fn from_str(shape: &str) -> Result<Self, Self::Err> {
        match shape {
            "A" | "X" => Ok(Shape::Rock),
            "B" | "Y" => Ok(Shape::Paper),
            "C" | "Z" => Ok(Shape::Scissors),
            _ => Err("Invalid shape.".to_string()),
        }
    }
}

/// Get score for rock, paper, scissors outcome.
///  Score: 0 = lost, 3 = draw, 6 = won
fn outcome_score(opponent: Shape, response: Shape) -> u32 {
    match (opponent, response) {
        (Shape::Rock, Shape::Rock) => 3,
        (Shape::Rock, Shape::Paper) => 6,
        (Shape::Rock, Shape::Scissors) => 0,
        (Shape::Paper, Shape::Rock) => 0,
        (Shape::Paper, Shape::Paper) => 3,
        (Shape::Paper, Shape::Scissors) => 6,
        (Shape::Scissors, Shape::Rock) => 6,
        (Shape::Scissors, Shape::Paper) => 0,
        (Shape::Scissors, Shape::Scissors) => 3,
    }
}

// Get score for shape played.
///  Score: Rock = 1, Paper = 2, Scissors = 3
fn shape_score(shape: Shape) -> u32 {
    match shape {
        Shape::Rock => 1,
        Shape::Paper => 2,
        Shape::Scissors => 3,
    }
}

fn score(opponent: Shape, response: Shape) -> u32 {
    outcome_score(opponent, response) + shape_score(response)
}

/// Determine total score for playing rock, paper, scissors with encrypted strategy guide.
///  Opponent: A = Rock, B = Paper, C = Scissors
///  Response: X = Rock, Y = Paper, Z = Scissors
///  Score: Rock = 1, Paper = 2, Scissors = 3
///         0 = lost, 3 = draw, 6 = won
fn part1(data: &str) -> u32 {
    data.lines()
        .map(|stategy| {
            let (opponent, response) = stategy.split_once(' ').unwrap();
            score(
                opponent.parse::<Shape>().unwrap(),
                response.parse::<Shape>().unwrap(),
            )
        })
        .sum()
}

/// Outcomes for the game rock, paper, scissors.
#[derive(Copy, Clone)]
enum Outcome {
    Lose,
    Draw,
    Win,
}

impl FromStr for Outcome {
    type Err = String;
    fn from_str(outcome: &str) -> Result<Self, Self::Err> {
        match outcome {
            "X" => Ok(Outcome::Lose),
            "Y" => Ok(Outcome::Draw),
            "Z" => Ok(Outcome::Win),
            _ => Err("Invalid outcome.".to_string()),
        }
    }
}

/// Determine shape to play in order to achieve desired game outcome.
///  X = lost, Y = draw, Z = win
fn required_response(opponent: Shape, desired_outcome: Outcome) -> Shape {
    match (opponent, desired_outcome) {
        (Shape::Rock, Outcome::Lose) => Shape::Scissors,
        (Shape::Rock, Outcome::Draw) => Shape::Rock,
        (Shape::Rock, Outcome::Win) => Shape::Paper,
        (Shape::Paper, Outcome::Lose) => Shape::Rock,
        (Shape::Paper, Outcome::Draw) => Shape::Paper,
        (Shape::Paper, Outcome::Win) => Shape::Scissors,
        (Shape::Scissors, Outcome::Lose) => Shape::Paper,
        (Shape::Scissors, Outcome::Draw) => Shape::Scissors,
        (Shape::Scissors, Outcome::Win) => Shape::Rock,
    }
}

/// Determine total score for playing rock, paper, scissors with correct strategy guide.
fn part2(data: &str) -> u32 {
    data.lines()
        .map(|stategy| {
            let (opponent, outcome) = stategy.split_once(' ').unwrap();
            let opponent = opponent.parse::<Shape>().unwrap();
            let outcome = outcome.parse::<Outcome>().unwrap();

            let response = required_response(opponent, outcome);
            score(opponent, response)
        })
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
        assert_eq!(results, 15)
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, 12)
    }
}
