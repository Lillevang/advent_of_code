# Author: Jeppe Lillevang Salling

ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'
LEFT_BOX = '['
RIGHT_BOX = ']'

MOVES = {
  '^' => {0, -1},
  '>' => {1, 0},
  'v' => {0, 1},
  '<' => {-1, 0},
}

# Add two tuples
def add_tuples(a : Tuple(Int32, Int32), b : Tuple(Int32, Int32)) : Tuple(Int32, Int32)
  {a[0] + b[0], a[1] + b[1]}
end

# Subtract two tuples
def sub_tuples(a : Tuple(Int32, Int32), b : Tuple(Int32, Int32)) : Tuple(Int32, Int32)
  {a[0] - b[0], a[1] - b[1]}
end

# Update cell value
def update_cell(grid : Array(Array(Char)), p : Tuple(Int32, Int32), item : Char)
  grid[p[1]][p[0]] = item
end

# Get cell value
def get_cell(grid : Array(Array(Char)), p : Tuple(Int32, Int32)) : Char
  grid[p[1]][p[0]]
end

# Iterate over all cells
def each_cell(grid : Array(Array(Char)), &block)
  grid.each_with_index do |row, y|
    row.each_with_index do |cell, x|
      yield cell, {x, y}
    end
  end
end

# Calculate the score of boxes
def boxes_score(grid : Array(Array(Char))) : Int32
  score = 0
  each_cell(grid) do |cell, p|
    score += p[0] + p[1] * 100 if cell == BOX || cell == LEFT_BOX
  end
  score
end

# Find starting position of the robot
def find_robot(grid : Array(Array(Char))) : Tuple(Int32, Int32)
  each_cell(grid) do |cell, p|
    return p if cell == ROBOT
  end
  raise "Robot not found on the grid"
end

# Check if a move is valid
def can_move?(grid : Array(Array(Char)), p1 : Tuple(Int32, Int32), p2 : Tuple(Int32, Int32)) : Bool
  case get_cell(grid, p2)
  when EMPTY
    true
  when WALL
    false
  else
    d = sub_tuples(p2, p1)
    if d == MOVES['<'] || d == MOVES['>']
      can_move?(grid, p2, add_tuples(p2, d))
    else
      other_half = get_cell(grid, p2) == LEFT_BOX ? add_tuples(p2, MOVES['>']) : add_tuples(p2, MOVES['<'])
      can_move?(grid, p2, add_tuples(p2, d)) && can_move?(grid, other_half, add_tuples(other_half, d))
    end
  end
end

# Move the robot or boxes
def move(grid : Array(Array(Char)), p1 : Tuple(Int32, Int32), p2 : Tuple(Int32, Int32)) : Tuple(Int32, Int32)
  thing = get_cell(grid, p1)
  case get_cell(grid, p2)
  when EMPTY
    update_cell(grid, p2, thing)
    update_cell(grid, p1, EMPTY)
    p2
  when WALL
    p1
  when BOX
    next_p = add_tuples(p2, sub_tuples(p2, p1))
    if p2 != move(grid, p2, next_p)
      update_cell(grid, p2, thing)
      update_cell(grid, p1, EMPTY)
      p2
    else
      p1
    end
  else # LEFT_BOX, RIGHT_BOX
    d = sub_tuples(p2, p1)
    if d == MOVES['<'] || d == MOVES['>']
      next_p = add_tuples(p2, d)
      if p2 != move(grid, p2, next_p)
        update_cell(grid, p2, thing)
        update_cell(grid, p1, EMPTY)
        p2
      else
        p1
      end
    else
      other_half = get_cell(grid, p2) == LEFT_BOX ? add_tuples(p2, MOVES['>']) : add_tuples(p2, MOVES['<'])
      if can_move?(grid, p2, add_tuples(p2, d)) && can_move?(grid, other_half, add_tuples(other_half, d))
        move(grid, p2, add_tuples(p2, d))
        move(grid, other_half, add_tuples(other_half, d))
        update_cell(grid, p1, EMPTY)
        update_cell(grid, p2, thing)
        update_cell(grid, other_half, EMPTY)
        p2
      else
        p1
      end
    end
  end
end

# Traverse the grid based on movements
def traverse(grid : Array(Array(Char)), movements : Array(Char))
  position = find_robot(grid)
  movements.each do |movement|
    direction = MOVES[movement]
    next_position = add_tuples(position, direction)
    position = move(grid, position, next_position)
  end
end

# Read input from a file
def read_input(file_path : String) : Tuple(Array(Array(Char)), Array(Char))
  grid = [] of Array(Char)
  movements = [] of Char
  File.open(file_path) do |file|
    reading_grid = true
    file.each_line do |line|
      if reading_grid
        if line.strip.empty?
          reading_grid = false
        else
          grid << line.strip.chars
        end
      else
        movements.concat(line.strip.chars)
      end
    end
  end
  {grid, movements}
end


# Main program
input_file = "input"
grid, movements = read_input(input_file)

part1_grid = grid.map(&.dup)
traverse(part1_grid, movements)
puts "Part 1 Score: #{boxes_score(part1_grid)}"

part2_grid = grid.map do |row|
  row.map do |cell|
    case cell
    when EMPTY
      [EMPTY, EMPTY]
    when BOX
      [LEFT_BOX, RIGHT_BOX]
    when WALL
      [WALL, WALL]
    when ROBOT
      [ROBOT, EMPTY]
    else
      raise "Unexpected cell type: #{cell}"
    end
  end.flatten
end
traverse(part2_grid, movements)
puts "Part 2 Score: #{boxes_score(part2_grid)}"
