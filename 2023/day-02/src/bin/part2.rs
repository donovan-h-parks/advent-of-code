use anyhow::{Context, Result};

fn main() -> Result<()> {
    let input = include_str!("./input.txt");
    let answer = process(input)?;
    println!("answer: {answer}");

    Ok(())
}

pub fn process(input: &str) -> Result<String> {
    let mut answer = 0;
    for game in input.lines() {
        let (_game_data, cube_reps) = game.split_once(':').context("valid game data")?;

        let mut min_red = 0;
        let mut min_green = 0;
        let mut min_blue = 0;
        for cube_stats in cube_reps.split(';') {
            for cube_stat in cube_stats.split(',') {
                let (num_cubes, color) = cube_stat
                    .trim()
                    .split_once(' ')
                    .context("valid cube data")?;

                let num_cubes = num_cubes.parse::<u32>()?;
                if color == "red" && num_cubes >= min_red {
                    min_red = num_cubes
                } else if color == "green" && num_cubes >= min_green {
                    min_green = num_cubes
                } else if color == "blue" && num_cubes >= min_blue {
                    min_blue = num_cubes
                }
            }
        }

        answer += min_red * min_green * min_blue;
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
        assert_eq!(answer, "2286");
    }
}
