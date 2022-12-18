use std::{collections::HashMap, fs};

use nom::{
    branch::alt,
    bytes::complete::{is_a, tag},
    character::complete::{self, alpha1, newline},
    multi::separated_list1,
    sequence::separated_pair,
    IResult,
};

#[derive(Debug)]
enum Command {
    Cd(ChangeDir),
    Ls(Vec<Files>),
}

#[derive(Debug)]
enum ChangeDir {
    Root,
    Up,
    Down(String),
}

#[derive(Debug)]
enum Files {
    File { size: u32 },
    Dir(String),
}

fn parse_cd(input: &str) -> IResult<&str, Command> {
    let (input, _) = tag("$ cd ")(input)?;
    let (input, dir) = alt((tag(".."), tag("/"), alpha1))(input)?;

    let change_dir = match dir {
        ".." => ChangeDir::Up,
        "/" => ChangeDir::Root,
        name => ChangeDir::Down(name.to_string()),
    };

    Ok((input, Command::Cd(change_dir)))
}

fn parse_file(input: &str) -> IResult<&str, Files> {
    let (input, (size, _name)) =
        separated_pair(complete::u32, tag(" "), is_a("qwertyuiopasdfghjklzxcvbnm."))(input)?;

    Ok((input, Files::File { size }))
}

fn parse_dir(input: &str) -> IResult<&str, Files> {
    let (input, _) = tag("dir ")(input)?;
    let (input, name) = alpha1(input)?;

    Ok((input, Files::Dir(name.to_string())))
}

fn parse_ls(input: &str) -> IResult<&str, Command> {
    let (input, _) = tag("$ ls")(input)?;
    let (input, _) = newline(input)?;
    let (input, files) = separated_list1(newline, alt((parse_file, parse_dir)))(input)?;

    Ok((input, Command::Ls(files)))
}

fn parse_commands(input: &str) -> IResult<&str, Vec<Command>> {
    let (input, cmds) = separated_list1(newline, alt((parse_ls, parse_cd)))(input)?;

    Ok((input, cmds))
}

fn calculate_sizes(
    (mut context, mut sizes): (Vec<String>, HashMap<Vec<String>, u32>),
    command: &Command,
) -> (Vec<String>, HashMap<Vec<String>, u32>) {
    match command {
        Command::Cd(ChangeDir::Root) => {
            context.push("".to_string());
        }
        Command::Cd(ChangeDir::Up) => {
            context.pop();
        }
        Command::Cd(ChangeDir::Down(name)) => {
            context.push(name.to_string());
        }
        Command::Ls(files) => {
            let sum = files
                .iter()
                .filter_map(|file| {
                    if let Files::File { size, .. } = file {
                        Some(size)
                    } else {
                        None
                    }
                })
                .sum::<u32>();

            for i in 0..context.len() {
                sizes
                    .entry(context[0..=i].to_vec())
                    .and_modify(|v| *v += sum)
                    .or_insert(sum);
            }
        }
    }

    (context, sizes)
}

fn part1(data: &str) -> u32 {
    let (_, cmds) = parse_commands(data).unwrap();

    let (_, sizes) = cmds.iter().fold((vec![], HashMap::new()), calculate_sizes);

    sizes
        .iter()
        .filter(|(_, &size)| size < 100000)
        .map(|(_, size)| size)
        .sum::<u32>()
}

fn part2(data: &str) -> u32 {
    let (_, cmds) = parse_commands(data).unwrap();

    let (_, sizes) = cmds.iter().fold((vec![], HashMap::new()), calculate_sizes);

    let total_size = 70_000_000;
    let needed_space = 30_000_000;

    let used_space = sizes.get(&vec!["".to_string()]).unwrap();

    let current_free_space = total_size - used_space;
    let need_to_free = needed_space - current_free_space;

    let mut valid_dirs = sizes
        .iter()
        .filter(|(_, &size)| size > need_to_free)
        .map(|(_, size)| size)
        .collect::<Vec<&u32>>();

    valid_dirs.sort();

    **valid_dirs.first().unwrap()
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
        assert_eq!(results, 95437)
    }

    #[test]
    fn test_part2() {
        let test_data = fs::read_to_string("test.dat").unwrap();
        let results = part2(&test_data);
        assert_eq!(results, 24933642)
    }
}
