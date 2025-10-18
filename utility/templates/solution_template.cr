def read_input : Array(String)
  File.read_lines("input")
end

def part_one(lines : Array(String)) : String
  # TODO: implement
  "part 1 not implemented (#{lines.size} lines)"
end

def part_two(lines : Array(String)) : String
  # TODO: implement
  "part 2 not implemented (#{lines.size} lines)"
end

lines = read_input
if ARGV.size > 0
  case ARGV[0]
  when "1"
    puts part_one(lines)
  when "2"
    puts part_two(lines)
  else
    puts part_one(lines)
    puts part_two(lines)
  end
else
  puts part_one(lines)
  puts part_two(lines)
end
