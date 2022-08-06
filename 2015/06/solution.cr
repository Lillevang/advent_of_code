struct Coordinate
    property x : Int32
    property y : Int32

    def initialize(coord_str : String)
        x, y = coord_str.split(",")
        @x = x.to_i32
        @y = y.to_i32
    end
end

def parse_instruction(instruction)
    turn_on = instruction.includes?("on")
    toggle = instruction.includes?("toggle")
    return turn_on, toggle
end

def process_instruction_generic(turn_on, toggle, from, to, grid_1, grid_2)
    (from.not_nil!.x..to.not_nil!.x).each do |x|
        (from.not_nil!.y..to.not_nil!.y).each do |y|
            coordinate = {x, y}
            unless grid_1.has_key?(coordinate)
                grid_1[coordinate] = 0
                grid_2[coordinate] = 0
            end
            if toggle
                grid_1[coordinate] = grid_1[coordinate] == 1 ? 0.to_i8 : 1.to_i8
                grid_2[coordinate] += 2
            elsif turn_on
                grid_1[coordinate] = 1
                grid_2[coordinate] += 1
            else
                grid_1[coordinate] = 0
                val = grid_2[coordinate] - 1
                grid_2[coordinate] = val < 0 ? 0 : val
            end
        end
    end
end

def create_coords(instruction)
    if from_str = instruction.match(/\d+,\d+/)
        from = Coordinate.new(from_str[0])
    end
    if to_str = instruction.match(/\d+,\d+$/)
        to = Coordinate.new(to_str[0])
    end
    return from, to
end

def solve(instructions)
    grid_1 = {} of Tuple(Int32, Int32) => Int8
    grid_2 = {} of Tuple(Int32, Int32) => Int32
    instructions.each do |instruction|
        turn_on, toggle = parse_instruction(instruction)
        from, to = create_coords(instruction)
        process_instruction_generic(turn_on, toggle, from, to, grid_1, grid_2)
    end
    return grid_1.values.reduce(0){ |acc, i| acc + i }, grid_2.values.reduce(0){ |acc, i| acc + i }
end

instructions = File.read_lines("./input")
part_1, part_2 = solve(instructions)
puts "Part one: #{part_1}"
puts "Part two: #{part_2}"
