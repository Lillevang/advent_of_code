input_data = File.read("./input")
current_position = {0, 0}
positions_visited = Set.new [current_position]

def process_move(current_position : Tuple(Int32, Int32), move : String)
    x = current_position[0]
    y = current_position[1]
    if move == "<"
        x = x - 1
    elsif move == ">"
        x = x + 1
    elsif move == "v"
        y = y - 1
    elsif move == "^"
        y = y + 1
    end
    return {x, y}
end

# Part One:
input_data.split("").each do |move|
    current_position = process_move(current_position, move)
    positions_visited.add(current_position)
end
p positions_visited.size

# Part Two:
s1_pos = {0,0}
s2_pos = {0,0}
positions_visited = Set.new [s1_pos, s2_pos]
input_data.split("").in_groups_of(2).each do |move_set|
    s1_pos = process_move(s1_pos, move_set[0].not_nil!)
    s2_pos = process_move(s2_pos, move_set[1].not_nil!)
    positions_visited.add(s1_pos)
    positions_visited.add(s2_pos)
end
p positions_visited.size