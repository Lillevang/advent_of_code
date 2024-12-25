use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

type s64 = i64;
type s32 = i32;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Op {
    And,
    Or,
    Xor,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Instr {
    a: String,
    b: String,
    op: Op,
    dst: String,
}

/// Reads a text file line-by-line into a Vec of Strings.
fn read_file_lines<P: AsRef<Path>>(path: P) -> Vec<String> {
    let file = File::open(path).expect("Unable to open file");
    let reader = BufReader::new(file);
    reader
        .lines()
        .map(|line| line.expect("Failed to read line"))
        .collect()
}

/// Splits a string by given separators (or whitespace), optionally skipping empty tokens.
/// For example, the snippet in the C++ code does something like:
///   `Split(lines[i], " :", KeepEmpty::No)`
/// We'll do a minimal imitation of that logic for demonstration.
fn split_string(s: &str, separators: &[char], keep_empty: bool) -> Vec<String> {
    let tokens = s.split(|c| separators.contains(&c));
    if keep_empty {
        tokens.map(|t| t.to_string()).collect()
    } else {
        tokens
            .filter(|t| !t.is_empty())
            .map(|t| t.to_string())
            .collect()
    }
}

/// Parse a &str as a signed 32-bit integer
fn as_s32(s: &str) -> s32 {
    s.parse::<s32>().unwrap()
}

/// Parse a &str as a signed 64-bit integer
fn as_s64(s: &str) -> s64 {
    s.parse::<s64>().unwrap()
}

pub fn run(file_path: &str) {
    // This will hold our Part 1 answer
    let mut p1: s64 = 0;

    // Read lines from file
    let lines = read_file_lines(file_path);

    // Map of known bool values
    let mut values: HashMap<String, bool> = HashMap::new();

    let mut bit_count: s64 = 0;
    let mut instructions: Vec<Instr> = Vec::new();

    // Phase 1: parse lines until we hit an empty line, which breaks. Then parse instructions.
    let mut i = 0;
    while i < lines.len() {
        if lines[i].trim().is_empty() {
            break;
        }
        // Example: "x00 : 1" => we might split on " :" ignoring empty
        let toks = split_string(&lines[i], &[' ', ':'], false);
        // C++: values[toks[0]] = bool(AsS32(toks[1]));
        values.insert(toks[0].clone(), as_s32(&toks[1]) != 0);
        i += 1;
    }

    // Now skip the blank line itself
    i += 1;

    // Parse instructions lines
    while i < lines.len() {
        let line = lines[i].trim();
        if line.is_empty() {
            i += 1;
            continue;
        }

        // tokens: e.g. "x00 AND y00 -> z00"
        // We might do something like: split by ' ', '->'
        // The C++ snippet used: Split(lines[i], " ->", KeepEmpty::No);
        let toks = split_string(line, &[' ', '-', '>'], false);
        // Example tokens might be: ["x00", "AND", "y00", "z00"]

        // If the first token starts with 'x', that increments bit_count
        if toks[0].starts_with('x') {
            bit_count += 1;
        }

        let op = match toks[1].as_str() {
            "AND" => Op::And,
            "OR" => Op::Or,
            "XOR" => Op::Xor,
            other => panic!("Unknown op: {}", other),
        };

        instructions.push(Instr {
            a: toks[0].clone(),
            b: toks[2].clone(),
            op,
            dst: toks[3].clone(),
        });

        i += 1;
    }

    // Make a copy for Part 2, because running Part 1 is destructive
    let mut instructions_p2 = instructions.clone();

    // Keep iterating over instructions until they are all resolved
    // (i.e., both operands exist in values, then we apply them, remove them, etc.)
    while !instructions.is_empty() {
        let mut idx = 0;
        while idx < instructions.len() {
            let inst = &instructions[idx];
            let found_a = values.get(&inst.a);
            let found_b = values.get(&inst.b);
            if found_a.is_none() || found_b.is_none() {
                idx += 1;
                continue;
            }
            let a = *found_a.unwrap();
            let b = *found_b.unwrap();

            let val = match inst.op {
                Op::And => a && b,
                Op::Or => a || b,
                Op::Xor => a ^ b,
            };
            values.insert(inst.dst.clone(), val);

            // remove the instruction
            instructions.remove(idx);
            // do not increment idx here because remove() shifts elements left
        }
    }

    // Build the Part 1 answer: for any key that starts with 'z', parse the numeric part after 'z'
    // as an index, shift the bit in the correct place.
    for (k, v) in &values {
        if k.starts_with('z') {
            // e.g. k = "z12" => parse "12" as i32
            let idx_str = &k[1..]; // skip 'z'
            let idx: s32 = as_s32(idx_str);
            if *v {
                p1 |= 1 << idx;
            }
        }
    }

    println!("P1: {}", p1);

    // ======================
    // Part 2
    // ======================
    // We have a known set of instructions that define an adder with x and y bits -> z bits, plus carry bits.
    // We'll categorize instructions the same way as in the C++ code.

    // We'll create new vectors:
    let mut xy_adds: Vec<Instr> = Vec::new();
    let mut xy_carries: Vec<Instr> = Vec::new();
    let mut z_outs: Vec<Instr> = Vec::new();
    let mut ands: Vec<Instr> = Vec::new();
    let mut carries: Vec<Instr> = Vec::new();

    for inst in &instructions_p2 {
        let a0 = inst.a.chars().next().unwrap_or('\0');
        let b0 = inst.b.chars().next().unwrap_or('\0');
        // If this instruction is about x or y
        if a0 == 'x' || a0 == 'y' || b0 == 'x' || b0 == 'y' {
            match inst.op {
                Op::Xor => xy_adds.push(inst.clone()),
                Op::And => xy_carries.push(inst.clone()),
                Op::Or => {
                    // The snippet doesn’t place an OR in the x/y logic, but we’ll just ignore.
                    // Or we can panic if we want. For now, ignore is consistent with original code’s logic.
                }
            }
            continue;
        }

        // Otherwise, it’s presumably in the second set
        match inst.op {
            Op::And => ands.push(inst.clone()),
            Op::Or => carries.push(inst.clone()),
            Op::Xor => z_outs.push(inst.clone()),
        }
    }

    // Now we do the checks to see which are “wrong.” The logic is the same as the snippet.
    let mut wrongs: Vec<String> = Vec::new();

    // XYAdd check
    for xy in &xy_adds {
        if xy.a == "x00" || xy.a == "y00" {
            // skip
            continue;
        }
        // If an XYAdd doesn't show up in the zOuts or if it writes to 'z' directly => wrong
        // We check if its output is used by a zOut as an input
        if xy.dst.starts_with('z')
            || !z_outs.iter().any(|z| z.a == xy.dst || z.b == xy.dst)
        {
            wrongs.push(xy.dst.clone());
        }
    }

    // XYCarry check
    for xy in &xy_carries {
        if xy.a == "x00" || xy.a == "y00" {
            // skip
            continue;
        }
        if xy.dst.starts_with('z')
            || !carries.iter().any(|c| c.a == xy.dst || c.b == xy.dst)
        {
            wrongs.push(xy.dst.clone());
        }
    }

    // zOut check
    for z in &z_outs {
        if !z.dst.starts_with('z') {
            wrongs.push(z.dst.clone());
        }
    }

    // carry check
    // The last carry is z{bit_count + 1}. If a carry has dst[0] == 'z' and it’s *not* that lastZ, it’s wrong.
    let last_z = format!("z{}", bit_count + 1);
    for c in &carries {
        if c.dst.starts_with('z') && c.dst != last_z {
            wrongs.push(c.dst.clone());
        }
    }

    // ANDs check: if the output is a 'z' register, that’s wrong.
    for a in &ands {
        if a.dst.starts_with('z') {
            wrongs.push(a.dst.clone());
        }
    }

    wrongs.sort();
    wrongs.dedup(); // optional, if you want to remove duplicates

    let p2 = wrongs.join(",");
    println!("P2: {}", p2);
}

fn main() {
    run("../input");
}
