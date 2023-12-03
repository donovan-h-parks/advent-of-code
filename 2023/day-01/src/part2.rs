const DIGIT_STRS: [(&str, &char); 9] = [
    ("one", &'1'),
    ("two", &'2'),
    ("three", &'3'),
    ("four", &'4'),
    ("five", &'5'),
    ("six", &'6'),
    ("seven", &'7'),
    ("eight", &'8'),
    ("nine", &'9'),
];

fn digit_name_to_digit(input: &str) -> String {
    let mut digitized_str = String::default();
    for line in input.lines() {
        let mut index = 0;
        while index < line.len() {
            let suffix = &line[index..];

            let mut result: Option<char> = None;
            if suffix.chars().next().is_some_and(|ch| ch.is_ascii_digit()) {
                result = suffix.chars().next();
            } else {
                for (digit_str, digit_ch) in DIGIT_STRS {
                    if suffix.starts_with(digit_str) {
                        result = Some(*digit_ch);
                        break;
                    }
                }
            }

            if let Some(num) = result {
                digitized_str.push(num);
            }

            index += 1;
        }

        digitized_str.push('\n');
    }

    digitized_str
}

pub fn process(input: &str) -> String {
    let input = digit_name_to_digit(input);

    let mut answer: u32 = 0;
    for line in input.lines() {
        let mut first_digit = char::default();
        let mut last_digit = char::default();
        for ch in line.chars() {
            if ch.is_ascii_digit() {
                if first_digit == char::default() {
                    first_digit = ch;
                    last_digit = ch;
                } else {
                    last_digit = ch;
                }
            }
        }

        answer += 10 * first_digit.to_digit(10).unwrap_or(0);
        answer += last_digit.to_digit(10).unwrap_or(0);
    }

    answer.to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_answer() {
        let input = include_str!("./test2.txt");
        let digitized_input = digit_name_to_digit(input);
        let answer = process(&digitized_input);
        assert_eq!(answer, "281");
    }
}
