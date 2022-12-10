use std::{fs, ops::RangeInclusive};

use nom::{
    bytes::complete::tag, character::complete, multi::separated_list1, sequence::separated_pair,
    IResult,
};

type Assignments = Vec<(RangeInclusive<u32>, RangeInclusive<u32>)>;

fn sections(input: &str) -> IResult<&str, RangeInclusive<u32>> {
    let (input, (start, end)) = separated_pair(complete::u32, tag("-"), complete::u32)(input)?;
    Ok((input, start..=end))
}

fn section_line(input: &str) -> IResult<&str, (RangeInclusive<u32>, RangeInclusive<u32>)> {
    let (input, assignment_pair) = separated_pair(sections, tag(","), sections)(input)?;
    Ok((input, assignment_pair))
}

fn section_assignments(input: &str) -> IResult<&str, Assignments> {
    let (input, ranges) = separated_list1(complete::newline, section_line)(input)?;
    Ok((input, ranges))
}

fn is_contained(range1: &RangeInclusive<u32>, range2: &RangeInclusive<u32>) -> bool {
    let contained12 = range1.contains(range2.start()) && range1.contains(range2.end());
    let contained21 = range2.contains(range1.start()) && range2.contains(range1.end());

    contained12 || contained21
}

fn is_overlap(range1: &RangeInclusive<u32>, range2: &RangeInclusive<u32>) -> bool {
    range1.contains(range2.start()) || range2.contains(range1.start())
}

fn part1(data: &str) -> u32 {
    let (_, assignments) = section_assignments(data).unwrap();

    let num_contained = assignments
        .iter()
        .map(|(assignment1, assignment2)| is_contained(assignment1, assignment2) as u32)
        .sum();

    num_contained
}

fn part2(data: &str) -> u32 {
    let (_, assignments) = section_assignments(data).unwrap();

    let num_overlap = assignments
        .iter()
        .map(|(assignment1, assignment2)| is_overlap(assignment1, assignment2) as u32)
        .sum();

    num_overlap
}

fn main() {
    let data = fs::read_to_string("./input.dat").unwrap();

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
        assert_eq!(results, 2)
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, 4)
    }
}
