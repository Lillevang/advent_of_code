use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::fs;

#[derive(PartialEq, Eq)]
struct State {
    score: usize,
    x: i32,
    y: i32,
    dx: i32,
    dy: i32,
    path: Vec<(i32, i32)>,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.score.cmp(&self.score)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

fn parse_input(file_path: &str) -> (Vec<u8>, usize, usize) {
    let input = fs::read_to_string(file_path).expect("Could not read file");
    let lines: Vec<&str> = input.lines().collect();
    let width = lines[0].len();
    let height = lines.len();
    let grid = lines.iter().flat_map(|&l| l.as_bytes()).copied().collect();
    (grid, width, height)
}

fn find_start(grid: &[u8], width: usize, height: usize) -> (i32, i32) {
    for y in 0..height {
        for x in 0..width {
            if grid[y * width + x] == b'S' {
                return (x as i32, y as i32);
            }
        }
    }
    panic!("Start position not found");
}

fn explore_paths(grid: &[u8], width: usize, height: usize, start: (i32, i32)) -> (usize, Vec<Vec<(i32, i32)>>) {
    let mut queue = BinaryHeap::new();
    queue.push(Reverse(State {
        score: 0,
        x: start.0,
        y: start.1,
        dx: 1,
        dy: 0,
        path: vec![(start.0, start.1)],
    }));

    let mut seen = vec![usize::MAX; width * height];
    let mut min_score = usize::MAX;
    let mut paths = Vec::new();

    while let Some(Reverse(state)) = queue.pop() {
        if grid[state.y as usize * width + state.x as usize] == b'E' {
            if state.score < min_score {
                min_score = state.score;
                paths.clear();
            }
            if state.score == min_score {
                paths.push(state.path.clone());
            }
            continue;
        }

        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let nx = state.x + dx;
            let ny = state.y + dy;

            if nx < 0 || ny < 0 || nx >= width as i32 || ny >= height as i32 {
                continue;
            }

            if grid[ny as usize * width + nx as usize] == b'#' {
                continue;
            }

            let nscore = if dx == state.dx && dy == state.dy {
                state.score + 1
            } else {
                state.score + 1001
            };

            let index = ny as usize * width + nx as usize;
            if nscore <= seen[index] {
                seen[index] = nscore;
                let mut new_path = state.path.clone();
                new_path.push((nx, ny));
                queue.push(Reverse(State {
                    score: nscore,
                    x: nx,
                    y: ny,
                    dx,
                    dy,
                    path: new_path,
                }));
            }
        }
    }

    (min_score, paths)
}

fn count_unique_positions(paths: &[Vec<(i32, i32)>], width: usize, height: usize) -> usize {
    let mut visited = vec![false; width * height];
    let mut count = 0;

    for path in paths {
        for &(x, y) in path {
            let index = y as usize * width + x as usize;
            if !visited[index] {
                visited[index] = true;
                count += 1;
            }
        }
    }

    count
}

fn main() {
    let (grid, width, height) = parse_input("../input");
    let start = find_start(&grid, width, height);

    let (min_score, paths) = explore_paths(&grid, width, height, start);
    let unique_positions = count_unique_positions(&paths, width, height);

    println!("Part 1: {}", min_score);
    println!("Part 2: {}", unique_positions + 1);
}
