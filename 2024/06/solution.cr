# TODO: Work in progress setting up the concurrency... similar to the go solution

class Vec
    property x : Int32
    property y : Int32

    def initialize(@x, @y)
    end

    def +(other : Vec) : Vec
        Vec.new(@x + other.x, @y + other.y)
    end

    def rotate(times : Int32) : Vec
        x = @x
        y = @y
        (0...(times % 4)).each do
            x, y = -y, x
        end
        Vec.new(x, y)
    end

    def ==(other : Vec) : Bool
        @x == other.x && @y == other.y
    end

    def hash
        {@x, @y}.hash
    end
end

class State
    property pos : Vec
    property dir : Vec

    def initialize(@pos, @dir)
    end

    def ==(other : State) : Bool
        @pos == other.pos && @dir == other.dir
    end

    def hash
        {@pos, @dir}.hash
    end
end


def parse_input(input : String) : Tuple(Array(Array(Char)), Vec)
    matrix = input.lines.map { |line| line.chars }
    start = matrix.each_with_index do |row, r|
        c = row.index('^')
        return Tuple.new(matrix, Vec.new(r,c)) if c
    end
    raise "No start position found"
end

def find_loop(matrix : Array(Array(Char)), start : Vec, obstruction : Vec) : Tuple(Bool, Set(Vec))
    visited_points = Set(Vec).new
    visited_states = Set(State).new

    current_position = start
    direction = Vec.new(-1, 0)

    loop do
        current_state = State.new(current_position, direction)

        # Detect loop
        if visited_states.includes?(current_state)
            return {true, visited_points}
        end

        # Track visited positions and states
        visited_points << current_position
        visited_states << current_state

        next_position = current_position + direction
        row, col = next_position.x, next_position.y

        # Check boundaries
        if row < 0 || row >= matrix.size || col < 0 || col >= matrix[0].size
            return {false, visited_points}
        end

        # Handle obstacles or obstruction
        if matrix[row][col] == '#' || next_position == obstruction
            # Rotate counter-clockwise if blocked
            direction = direction.rotate(3)
        else
            # Move to the next position
            current_position = next_position
        end
    end
end

input = File.read("input_sample").chomp
matrix, start = parse_input(input)
original_path = find_loop(matrix, start, Vec.new(-1, -1))
puts original_path[1].size
