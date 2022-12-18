use std::fs;

use nom::{
    branch::alt,
    bytes::complete::tag,
    character::complete::{self, alpha1, digit1, multispace1, newline},
    multi::{many1, separated_list1},
    sequence::{delimited, preceded},
    IResult,
};

#[derive(Debug)]
struct MoveInstruction {
    number: u32,
    from: u32,
    to: u32,
}

fn parse_crate(input: &str) -> IResult<&str, Option<&str>> {
    let (input, crate_name) = alt((tag("   "), delimited(tag("["), alpha1, tag("]"))))(input)?;

    let crate_name = match crate_name {
        "   " => None,
        value => Some(value),
    };

    Ok((input, crate_name))
}

fn parse_crate_row(input: &str) -> IResult<&str, Vec<Option<&str>>> {
    separated_list1(tag(" "), parse_crate)(input)
}

fn parse_move_instruction(input: &str) -> IResult<&str, MoveInstruction> {
    let (input, _) = tag("move ")(input)?;
    let (input, number) = complete::u32(input)?;
    let (input, _) = tag(" from ")(input)?;
    let (input, from) = complete::u32(input)?;
    let (input, _) = tag(" to ")(input)?;
    let (input, to) = complete::u32(input)?;

    Ok((
        input,
        MoveInstruction {
            number,
            from: from - 1,
            to: to - 1,
        },
    ))
}

fn parse_stacks(input: &str) -> IResult<&str, (Vec<Vec<&str>>, Vec<MoveInstruction>)> {
    let (input, crate_rows) = separated_list1(newline, parse_crate_row)(input)?;

    let (input, stack_nums) = many1(preceded(multispace1, digit1))(input)?;

    let (input, _) = multispace1(input)?;

    let (input, move_instructions) = separated_list1(newline, parse_move_instruction)(input)?;

    let mut stacks = vec![];
    for _ in 0..stack_nums.len() {
        stacks.push(vec![]);
    }

    for row in crate_rows.iter().rev() {
        for (idx, crate_name) in row.iter().enumerate() {
            if crate_name.is_some() {
                stacks[idx].push(crate_name.unwrap());
            }
        }
    }

    Ok((input, (stacks, move_instructions)))
}

fn part1(data: &str) -> String {
    let (_, (mut stacks, move_instructions)) = parse_stacks(data).unwrap();

    for MoveInstruction { number, from, to } in move_instructions {
        for _ in 0..number {
            let crate_name = stacks[(from) as usize].pop().unwrap();
            stacks[(to) as usize].push(crate_name);
        }
    }

    let mut top_crates = String::new();
    for mut stack in stacks {
        top_crates += stack.pop().unwrap();
    }

    top_crates
}

fn part2(data: &str) -> String {
    let (_, (mut stacks, move_instructions)) = parse_stacks(data).unwrap();

    for MoveInstruction { number, from, to } in move_instructions {
        let stack_len = stacks[from as usize].len();
        let mut x = stacks[from as usize]
            .drain(stack_len - number as usize..)
            .collect::<Vec<&str>>();
        stacks[to as usize].append(&mut x);
    }

    let mut top_crates = String::new();
    for mut stack in stacks {
        top_crates += stack.pop().unwrap();
    }

    top_crates
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
        assert_eq!(results, "CMZ")
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, "MCD")
    }
}
