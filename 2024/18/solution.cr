require "collections"

# Read coordinates from input file
coordinates = File.read("input").strip.split("\n").map do |line|
  line.split(",").map(&.to_i)
end

# Initialize a 71x71 grid
grid = Collections::Grid.new(71, 71, false)

# Initialize variables for results
part1_distance = nil
part1_path = [] of Collections::Grid::Point
part2_coordinate = nil

# Start and goal positions
start = {0,0}
goal = {70,70}

# Iterate over all coordinates
coordinates.each_with_index do |coordinate, index|
  x, y = coordinate[0], coordinate[1]

  if x >= 0 && x < 71 && y >= 0 && y < 71
    grid.set(x, y, true) # Block the coordinate
  else
    puts "Skipping invalid coordinate: (#{x}, #{y})"
    next
  end

  if index == 1023
    # Calculate Part 1 result after blocking the first 1024 coordinates
    result = grid.shortest_path(start, goal)
    if result
      part1_distance, part1_path = result
      grid.print_grid(part1_path) if part1_path
      puts "Part 1 - Shortest path: #{part1_distance}" if part1_distance
    else
      puts "Part 1 - No path found"
    end
  end

  # Start checking for Part 2 after Part 1 is calculated
  if index >= 1024
    # Check if goal is still reachable
    result = grid.shortest_path(goal, start) # Reverse search
    unless result
      part2_coordinate = coordinate
      break
    end
  end
end

# Output final results
puts "Part 2 - First coordinate that makes goal unreachable: (#{part2_coordinate[0]}, #{part2_coordinate[1]})" if part2_coordinate
