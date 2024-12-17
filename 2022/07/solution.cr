
lines = File.read("./input").strip().split("\n")
dirs = Hash(String, Int64).new(0)
cwd = [] of String

lines.each do |line|
  cwd = ["/"] if line == "$ cd /"
  cur_line = line.split()
  next if (cur_line[0]  == "$" && cur_line[1] == "ls") || cur_line[0] == "dir"
  if cur_line[0] == "$" && cur_line[1] == "cd" && cur_line[2] == ".."
    cwd.pop
  elsif cur_line[0] == "$" && cur_line[1] == "cd" && cur_line[2] != ".."
    cwd << "#{cur_line[2]}/"
  else
    path = ""
    cwd.each do |d|
      path = path + d
      dirs[path] = dirs[path] + cur_line[0].to_i64
    end
  end
end

# part 1:
puts dirs.values.select { |v| v <= 100000 }.sum

# part 2:
puts dirs.values.select { |v| v >= dirs["/"] - 40000000 }.min
