const MAX_RED: u32 = 12;
const MAX_GREEN: u32 = 13;
const MAX_BLUE: u32 = 14;

fn main() {
    let input = include_str!("./input.txt");
    let answer = process(input);
    println!("answer: {answer}");
}

pub fn process(input: &str) -> String {
    let mut answer = 0;
    for game in input.lines() {
        let (game_data, cube_reps) = game.split_once(':').expect("valid game data");

        let mut valid_game = true;
        for cube_stats in cube_reps.split(';') {
            for cube_stat in cube_stats.split(',') {
                let (num_cubes, color) = cube_stat.trim().split_once(' ').expect("valid cube data");

                let valid = match color {
                    "red" => num_cubes.parse::<u32>().expect("valid cube number") <= MAX_RED,
                    "green" => num_cubes.parse::<u32>().expect("valid cube number") <= MAX_GREEN,
                    "blue" => num_cubes.parse::<u32>().expect("valid cube number") <= MAX_BLUE,
                    _ => false,
                };

                if !valid {
                    valid_game = false;
                    break;
                }
            }

            if !valid_game {
                break;
            }
        }

        if valid_game {
            let (_game, game_num) = game_data.split_once(' ').expect("valid game data");
            answer += game_num.parse::<u32>().expect("valid game number");
        }
    }

    answer.to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_answer() {
        let input = include_str!("./test.txt");
        let answer = process(input);
        assert_eq!(answer, "8");
    }
}
