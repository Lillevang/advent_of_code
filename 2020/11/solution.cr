require "../../utility/crystal/grid_padder.cr"

module Solution
  extend self

  def read_input
    File.read("input")
      .split("\n")
      .select{|n| n != ""}
  end

  # Adds padding of "ground" spaces
  def pad_grid(data : Array(String)) : Array(Array(Char))
    GridPadder.pad_grid(data, ".").map(&.chars)
  end

  # Grid is padded, start at 1,1 and move to (grid.size - 1 grid[0].size - 1). Check adjacanct cells for each position in grid
  def evolve_grid(grid : Array(Array(Char))) : Array(Array(Char))
    new_state = [] of Array(Char)
    new_state << ['.'] * grid[0].size
    (1...(grid.size - 1)).each do |y|
      new_row = ['.']
      (1...(grid[0].size - 1)).each do |x|
        new_row << check_adjacent(grid, {x, y})
      end
      new_row << '.'
    new_state << new_row
    end
    new_state << ['.'] * grid[0].size
    new_state
  end

  # Checks adjacent cells and returns the evolved state for that position
  def check_adjacent(grid : Array(Array(Char)), cur_pos : Tuple(Int32, Int32))
    cur_status = grid[cur_pos[1]][cur_pos[0]]
    return cur_status if cur_status == '.'
    number_of_occupied_adjacent_seats = 0
    adj_above = grid[(cur_pos[1] - 1)][(cur_pos[0]-1)...(cur_pos[0]+1)].count('#')
    adj_left = grid[cur_pos[1]][cur_pos[0] - 1] == '#' ? 1 : 0
    adj_right = grid[cur_pos[1]][cur_pos[0] + 1] == '#' ? 1 : 0
    adj_below = grid[(cur_pos[1] - +1)][(cur_pos[0]-1)...(cur_pos[0]+1)].count('#')
    number_of_occupied_adjacent_seats += adj_above
    number_of_occupied_adjacent_seats += adj_below
    number_of_occupied_adjacent_seats += adj_left
    number_of_occupied_adjacent_seats += adj_right
    if cur_status == 'L' && number_of_occupied_adjacent_seats == 0
      return '#'
    elsif cur_status == '#' && number_of_occupied_adjacent_seats >= 4
      return 'L'
    else
      return cur_status
    end
  end

  # Counts "#" in total in grid
  def count_occupied_seats(grid : Array(Array(Char)))
    p ""
  end

  def part_one
    grid = pad_grid
    new_grid = evolve_grid(grid)

    # TODO: set grid = new_grid and evolve again until state is settled

    # Termination check:
    if grid == new_grid
      p count_occupied_seats
    end
  end
end


#grid = Solution.pad_grid(Solution.read_input)
#p "Col length: #{grid.size}"
#p "Row length: #{grid[0].size}"
#grid.each do |l|
#  p l
#end
