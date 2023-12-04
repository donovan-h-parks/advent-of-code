use anyhow::Result;
use itertools::Itertools;

fn main() -> Result<()> {
    let input = include_str!("./input.txt");
    let answer = process(input)?;
    println!("answer: {answer}");

    Ok(())
}

fn adjacent_gear(map: &Vec<Vec<char>>, row_num: usize, col_num: usize) -> Option<(usize, usize)> {
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
            if r < map.len() && c < map[0].len() && map[r][c] == '*' {
                return Some((c, r));
            }
        }
    }

    None
}

#[derive(Debug, Default, PartialEq)]
struct Part {
    is_gear: bool,
    row: usize,
    col: usize,
    value: String,
}

pub fn process(input: &str) -> Result<String> {
    let map: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();

    let mut gears = Vec::new();
    for (row_num, row) in map.iter().enumerate() {
        let mut cur_part = Part::default();
        for (col_num, ch) in row.iter().enumerate() {
            if ch.is_ascii_digit() {
                cur_part.value.push(*ch);
                if let Some((gear_row, gear_col)) = adjacent_gear(&map, row_num, col_num) {
                    cur_part.is_gear = true;
                    cur_part.row = gear_row;
                    cur_part.col = gear_col;
                }
            } else {
                if cur_part.is_gear {
                    gears.push(cur_part);
                }

                cur_part = Part::default();
            }
        }

        if cur_part.is_gear {
            gears.push(cur_part);
        }
    }

    let mut answer: u64 = 0;
    for gears in gears.iter().combinations(2) {
        if gears[0].row == gears[1].row && gears[0].col == gears[1].col {
            answer += gears[0].value.parse::<u64>()? * gears[1].value.parse::<u64>()?;
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
        assert_eq!(answer, "467835");
    }
}
