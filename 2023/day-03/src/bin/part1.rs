use anyhow::Result;

fn main() -> Result<()> {
    let input = include_str!("./input.txt");
    let answer = process(input)?;
    println!("answer: {answer}");

    Ok(())
}

fn adjacent_symbol(map: &Vec<&str>, row_num: usize, col_num: usize) -> bool {
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
            if r < map.len() && c < map[0].len() {
                let test_ch = map[r].chars().nth(c).unwrap_or('.');
                if !test_ch.is_ascii_digit() && test_ch != '.' {
                    return true;
                }
            }
        }
    }

    false
}

pub fn process(input: &str) -> Result<String> {
    let mut answer: u64 = 0;

    let map: Vec<_> = input.lines().collect();

    for (row_num, row) in map.iter().enumerate() {
        let mut is_part = false;
        let mut part_num = String::default();
        for (col_num, ch) in row.chars().enumerate() {
            if ch.is_ascii_digit() {
                part_num.push(ch);
                if adjacent_symbol(&map, row_num, col_num) {
                    is_part = true;
                }
            } else {
                if !part_num.is_empty() && is_part {
                    answer += part_num.parse::<u64>()?;
                }

                part_num.clear();
                is_part = false;
            }
        }

        if !part_num.is_empty() && is_part {
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
