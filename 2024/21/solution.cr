require "collections"

# Type Aliases
alias Position = Tuple(Int32, Int32)
alias PathString = String
alias Cost = Int32
alias QueueState = Array(Int32 | Position | String)

# Constants
KEYPAD_MAIN = ["789", "456", "123", " 0A"]
KEYPAD_NAVIGATION = [" ^A", "<v>"]
MOVES = ["^", "<", "v", ">", "A"]
START_POSITIONS = {
    "^" => {0, 1},
    "<" => {1, 0},
    "v" => {1, 1},
    ">" => {1, 2},
    "A" => {0, 2}
}
MOVE_CACHE = Hash[Tuple[str, str, int], int].new

def find_shortest_path(target_code : String, pad_depth : Int32) : Int32
  # Initial state with type QueueState
  initial_state : QueueState = [0, {3, 2}, "A", "", ""]
  queue = Collections::BinaryHeapMin(Array(QueueState)).new.add([initial_state])
  visited = Hash({Position, String, String}, Int32).new

  while queue.size > 0
    distance, current_position, current_direction, current_output, path = queue.extract_root!
    puts "Distance: #{distance}, Position: #{current_position}, Direction: #{current_direction}, Output: #{current_output}, Path: #{path}"
    exit 1
  end

  0
end


p1, p2 = 0, 0
data = File.read_lines("input_sample")

data.each do |line|
  s1 = find_shortest_path(line, 2)
  s2 = find_shortest_path(line, 25)
  line_integers = Regex.new("-?\\d+").match(line).to_s.to_i
  p1 += line_integers * s1
  p2 += line_integers * s2
end

puts p1
puts p2
