
data = File.read("./input").strip().split("\n")

keyword_vals = {"noop" => 0, "addx" => 0}
sanitized_input = [1]

data.each do |x|
  x.split().each do |w|
    val = keyword_vals.has_key?(w) ? keyword_vals[w] : w.strip().to_i
    sanitized_input << val
  end
end

part1 = 0
part2 = "\n"
sanitized_input.accumulate.each_with_index(1) do |x, i|
  part1 += i%40==20 ? i*x : 0
  part2 += [-1,0,1].includes?((i-1)%40-x) ? "#" : " "
end

puts part1

# Ugly printing... Drag the console until the letters form
part2.chars.each do |c|
  print c + " "
end
puts
