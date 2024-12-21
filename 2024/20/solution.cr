require "complex"

# Initialize variables
start, target, map = nil, nil, Set(Complex).new

# Read input and parse the map
# '#' represents walls; 'S' is the start, 'E' is the target.
File.read_lines("input").each_with_index do |line, y|
  line.chars.each.with_index do |char, x|
    point = Complex.new(x, y) # Complex number represents (x, y) coordinates
    map << point unless char == '#'
    start = point if char == 'S'
    target = point if char == 'E'
  end
end

# Directions for navigation: right, up, left, down
# Represented as complex numbers:
# 1+0.i (right), 0-1.i (up), -1+0.i (left), 0+1.i (down)
DIRS = [1 + 0.0.i, 0 - 1.0.i, -1 + 0.0.i, 0 + 1.0.i]

# Initialize distance hash and queue for BFS
dist = Hash(Complex, Int32).new
dist[target] = 0 if target
queue = [target]
visited = Set(Complex).new

# Perform Breadth-First Search (BFS) to calculate shortest distances
until queue.empty?
  node = queue.pop
  if node
    visited << node
    # Navigate to neighbors using DIRS
    DIRS.map { |dir| node + dir } # Add direction to current position
      .select { |pos| map.includes?(pos) && !visited.includes?(pos) } # Select valid neighbors
      .each do |pos|
        dist[pos] = dist[node] + 1  # Update distance to neighbor
        queue << pos                # Add neighbor to the queue
      end
  end
end

# Manhattan distance calculation between two points
def manhattan(a, b)
  (a.real - b.real).abs + (a.imag - b.imag).abs
end

# Count pairs of points within a given cheat size
# Cheatsize is the maximum Manhattan distance to consider
def count(cheat_size, dist)
  dist.keys.combinations(2) # Generate all pairs of points
    .select { |pair| manhattan(pair[0], pair[1]) <= cheat_size } # Filter by Manhattan distance
    .count { |pair| dist[pair[1]] - dist[pair[0]] >= manhattan(pair[0], pair[1]) + 100 }
end

# Part 1: Small cheat size
puts "Part 1 result: #{count(2, dist)}"

# Part 2: Larger cheat size
puts "Part 2 result: #{count(20, dist)}"
