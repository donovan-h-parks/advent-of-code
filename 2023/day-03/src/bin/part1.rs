use anyhow::Result;

fn main() -> Result<()> {
    let input = include_str!("./input.txt");
    let answer = process(input)?;
    println!("answer: {answer}");

    Ok(())
}

fn adjacent_symbol(map: &Vec<Vec<char>>, row_num: usize, col_num: usize) -> bool {
    let mut row_min = 0;
    if row_num > 1 {
        row_min = row_num - 1;
    }

    let mut col_min = 0;
    if col_num > 1 {
        col_min = col_num - 1;
    }

    for r in row_min..=(row_num + 1) {
        for c in col_min..=(col_num + 1) {
            if r < map.len() && c < map[0].len() && !map[r][c].is_ascii_digit() && map[r][c] != '.'
            {
                return true;
            }
        }
    }

    false
}

pub fn process(input: &str) -> Result<String> {
    let mut answer: u64 = 0;

    let map: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();

    for (row_num, row) in map.iter().enumerate() {
        let mut is_part = false;
        let mut part_num = String::default();
        for (col_num, ch) in row.iter().enumerate() {
            if ch.is_ascii_digit() {
                part_num.push(*ch);
                if adjacent_symbol(&map, row_num, col_num) {
                    is_part = true;
                }
            } else {
                if is_part {
                    answer += part_num.parse::<u64>()?;
                }

                part_num.clear();
                is_part = false;
            }
        }

        if is_part {
            answer += part_num.parse::<u64>()?;
        }
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
        assert_eq!(answer, "4361");
    }
}
