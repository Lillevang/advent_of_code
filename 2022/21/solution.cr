
class Solver

  @@values = Hash(String, Float32 | Float64 | Int64).new
  @@operations = Hash(String, Array(String)).new

  def initialize(values, operations, part = "1")
    @@values = values.clone
    @@operations = operations.clone
    if part == "1"
      part_one
      puts @@values["root"].to_i64
    elsif part == "2"
      puts part_two
    end
  end

  def eval_to_int(op, left, right)
    if op == "+"
      left + right
    elsif op == "-"
      left - right
    elsif op == "*"
      left * right
    elsif op == "/"
      left // right
    else
      raise Exception.new("Unknown operation: #{left}#{op}#{right}")
    end
  end

  def part_one
    # TODO : Low hanging performance improvement would be to cache the values that have been updated to avoid redundant evals
    while !@@values.has_key?("root")
      valid_operations = @@operations.select { |_, v| @@values.has_key?(v[1]) && @@values.has_key?(v[2]) }
      valid_operations.each { |k,v| @@values[k] = eval_to_int(v[0], @@values[v[1]], @@values[v[2]]) }
    end
  end

  # Implementation of binary search to determine the value of humn
  def part_two
    high = 5000000000000
    low = 0.to_i64
    cur_guess = high // 2
    values = @@values.clone
    values["humn"] = cur_guess
    found = false
    while !found
      valid_operations = @@operations.select { |_, v| values.has_key?(v[1]) && values.has_key?(v[2]) }
      valid_operations.each { |k,v|
        if k != "root"
          values[k] = eval_to_int(v[0], values[v[1]], values[v[2]])
        else
          left = values[v[1]]
          right = values[v[2]]
          return cur_guess if values[v[1]] == values[v[2]]
          if left < right
            high = cur_guess - 1
            cur_guess = (low + high) // 2
          else
            low = cur_guess + 1
            cur_guess = (low + high) // 2
          end
          values = @@values.clone
          values["humn"] = cur_guess
          break
        end
        }
    end
  end
end

# Single file parse to improve performance
def parse_input(path = "./input")
  values = Hash(String, Float32| Float64 | Int64).new
  operations = Hash(String, Array(String)).new

  File.read(path).strip().split("\n").each do |line|
    if md = line.match(/(\w+): (\d+)/)
      values[md[1]] = md[2].to_i64
    elsif md = line.match(/(\w+): (\w+) (.) (\w+)/)
      operations[md[1]] = [md[3], md[2], md[4]]
    else
      raise Exception.new("Unrecognized command: #{line}")
      exit 1
    end
  end
  return values, operations
end

values, operations = parse_input
Solver.new(values, operations)
Solver.new(values, operations, "2")
