use std::env;
use std::fs;

fn read_input() -> Vec<String> {
    let data = fs::read_to_string("input").expect("failed to read input");
    data.lines().map(|s| s.to_string()).collect()
}

fn part_one(lines: &[String]) -> String {
    // TODO: implement
    format!("part 1 not implemented ({} lines)", lines.len())
}

fn part_two(lines: &[String]) -> String {
    // TODO: implement
    format!("part 2 not implemented ({} lines)", lines.len())
}

fn main() {
    let lines = read_input();
    let arg = env::args().nth(1);
    match arg.as_deref() {
        Some("1") => println!("{}", part_one(&lines)),
        Some("2") => println!("{}", part_two(&lines)),
        _ => {
            println!("{}", part_one(&lines));
            println!("{}", part_two(&lines));
        }
    }
}
