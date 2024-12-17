DATA = File.read("input").chomp
DIRS = [{-1, 0}, {0, 1}, {1, 0}, {0, -1}]
GRID = DATA.lines
ROW_LEN = GRID.size
COL_LEN = GRID[0].size

def explore_region(row : Int32, col : Int32, seen : Set(Tuple(Int32, Int32)), queue : Array(Tuple(Int32, Int32)), perimeter_hash : Hash(Tuple(Int32, Int32), Set(Tuple(Int32, Int32)))) : Tuple(Int32, Int32)
  area = 0
  perimeter = 0
  while queue.size > 0
    current_row, current_col = queue.shift
    next if seen.includes?({current_row, current_col})
    seen << {current_row, current_col}
    area += 1
    DIRS.each do |delta_row, delta_col|
      neighbor_row = current_row + delta_row
      neighbor_col = current_col + delta_col
      if 0 <= neighbor_row < ROW_LEN && 0 <= neighbor_col < COL_LEN && GRID[neighbor_row][neighbor_col] == GRID[current_row][current_col]
        queue << {neighbor_row, neighbor_col}
      else
        perimeter += 1
        if !perimeter_hash.has_key?({delta_row, delta_col})
          perimeter_hash[{delta_row, delta_col}] = Set(Tuple(Int32, Int32)).new
        end
        perimeter_hash[{delta_row, delta_col}] << {current_row, current_col}
      end
    end
  end
  {area, perimeter}
end

def calculate_sides(perimeter_hash : Hash(Tuple(Int32, Int32), Set(Tuple(Int32, Int32)))) : Int32
  sides = 0
  perimeter_hash.each do |direction, cells|
    seen_perimeter = Set(Tuple(Int32, Int32)).new
    cells.each do |perimeter_row, perimeter_col|
      if !seen_perimeter.includes?({perimeter_row, perimeter_col})
        sides += 1
        queue = [{perimeter_row, perimeter_col}]
        while queue.size > 0
          current_row, current_col = queue.shift
          next if seen_perimeter.includes?({current_row, current_col})
          seen_perimeter << {current_row, current_col}
          DIRS.each do |delta_row, delta_col|
            neighbor_row = current_row + delta_row
            neighbor_col = current_col + delta_col
            if cells.includes?({neighbor_row, neighbor_col})
              queue << {neighbor_row, neighbor_col}
            end
          end
        end
      end
    end
  end
  sides
end

part_1 = 0
part_2 = 0
seen = Set(Tuple(Int32, Int32)).new

(0...ROW_LEN).each do |row|
  (0...COL_LEN).each do |col|
    next if seen.includes?({row, col})
    queue = [{row, col}]
    perimeter_hash = Hash(Tuple(Int32, Int32), Set(Tuple(Int32, Int32))).new
    area, perimeter = explore_region(row, col, seen, queue, perimeter_hash)

    # Part 2
    sides = calculate_sides(perimeter_hash)
    part_1 += area * perimeter
    part_2 += area * sides
  end
end

puts part_1
puts part_2
