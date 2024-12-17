# Read and parse the input
input = File.read("input").chomp
grid = input.lines.map { |line| line.chars }

# Grid dimensions
x = grid.size
y = grid[0].size

# Initialize data structures
antinodes = Set(Tuple(Int32, Int32)).new
antinodes_2 = Set(Tuple(Int32, Int32)).new
nodes = Hash(Char, Array(Tuple(Int32, Int32))).new

# Populate nodes from the grid
0.upto(x - 1) do |i|
  0.upto(y - 1) do |j|
    char = grid[i][j]
    next if char == '.'

    nodes[char] ||= [] of Tuple(Int32, Int32)
    nodes[char] << {i, j}
  end
end

# Define methods
def calculate_antinode(
  pr1 : Tuple(Int32, Int32),
  pr2 : Tuple(Int32, Int32),
  x : Int32,
  y : Int32,
  antinodes : Set(Tuple(Int32, Int32)),
  extended : Bool = false
) : Nil
  x1, y1 = pr1
  x2, y2 = pr2

  # Add the initial point for extended antinode calculation
  antinodes << {x2, y2} if extended

  dx = x2 + (x2 - x1)
  dy = y2 + (y2 - y1)

  while dx >= 0 && dx < x && dy >= 0 && dy < y
    antinodes << {dx, dy}
    break unless extended
    dx += (x2 - x1)
    dy += (y2 - y1)
  end
end

# Process each pair of nodes
nodes.each do |_, positions|
  l = positions.size

  (0...l).each do |i|
    (0...i).each do |j|
      node1 = positions[i]
      node2 = positions[j]

      # Calculate antinodes
      calculate_antinode(node1, node2, x, y, antinodes)
      calculate_antinode(node2, node1, x, y, antinodes)

      # Calculate extended antinodes
      calculate_antinode(node1, node2, x, y, antinodes_2, true)
      calculate_antinode(node2, node1, x, y, antinodes_2, true)
    end
  end
end

# Output results
puts "Part 1: #{antinodes.size}"
puts "Part 2: #{antinodes_2.size}"
