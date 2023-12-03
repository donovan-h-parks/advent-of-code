pub fn process(input: &str) -> String {
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
        let input = include_str!("./test1.txt");
        let answer = process(input);
        assert_eq!(answer, "142");
    }
}
