require "collections"

# Input handling
def parse_input(file_path : String) : Tuple(Array(Array(Char)), Int32, Int32, Int32, Int32)
  grid = File.read(file_path).strip.split("\n").map(&.chars)
  start_row, start_col, end_row, end_col = 0, 0, 0, 0

  grid.each_with_index do |row, r|
    row.each_with_index do |cell, c|
      if cell == 'S'
        start_row, start_col = r, c
      elsif cell == 'E'
        end_row, end_col = r, c
      end
    end
  end

  {grid, start_row, start_col, end_row, end_col}
end

# Dijkstra's algorithm
def dijkstra(
  grid : Array(Array(Char)),
  start_row : Int32,
  start_col : Int32,
  initial_directions : Array(Int32),
  forward : Bool
) : Hash(Tuple(Int32, Int32, Int32), Int32)
  row_count = grid.size
  col_count = grid[0].size

  # Direction vectors: Up, Right, Down, Left
  directions = [
    {-1, 0}, # Up
    {0, 1},  # Right
    {1, 0},  # Down
    {0, -1}  # Left
  ]

  # Priority queue and data structures
  heap = Collections::BinaryHeapMin(Tuple(Int32, Int32, Int32, Int32)).new
  visited = Set(Tuple(Int32, Int32, Int32)).new
  distances = Hash(Tuple(Int32, Int32, Int32), Int32).new

  # Initialize the heap
  initial_directions.each do |dir|
    heap.add({0, start_row, start_col, dir})
  end

  # Process the queue
  while heap.size > 0
    distance, row, col, direction = heap.extract_root!

    # Record distance
    unless distances.has_key?({row, col, direction})
      distances[{row, col, direction}] = distance
    end

    # Skip if already visited
    next unless visited.add?({row, col, direction})

    # Move in the current direction
    dr, dc = forward ? directions[direction] : directions[(direction + 2) % 4]
    next_row, next_col = row + dr, col + dc
    if next_row >= 0 && next_row < row_count && next_col >= 0 && next_col < col_count && grid[next_row][next_col] != '#'
      heap.add({distance + 1, next_row, next_col, direction})
    end

    # Turn left or right
    heap.add({distance + 1000, row, col, (direction + 1) % 4}) # Turn right
    heap.add({distance + 1000, row, col, (direction + 3) % 4}) # Turn left
  end

  distances
end

# Main execution
file_path = "../data/input"
grid, start_row, start_col, end_row, end_col = parse_input(file_path)

# Part 1: Shortest path from start to end
distances = dijkstra(grid, start_row, start_col, [0, 1, 2, 3], true)

# Determine the best distance to the endpoint
best_distance = (0...4).map do |dir|
  distances[{end_row, end_col, dir}]
end.compact.min

puts "Part 1: #{best_distance}"

# Part 2: Reverse Dijkstra and count optimal paths
distances2 = dijkstra(grid, end_row, end_col, [0, 1, 2, 3], false)

optimal_paths = Set(Tuple(Int32, Int32)).new
(0...grid.size).each do |row|
  (0...grid[0].size).each do |col|
    (0...4).each do |dir|
      if distances.has_key?({row, col, dir}) &&
         distances2.has_key?({row, col, dir}) &&
         distances[{row, col, dir}] + distances2[{row, col, dir}] == best_distance
        optimal_paths.add({row, col})
      end
    end
  end
end

puts "Part 2: #{optimal_paths.size}"
