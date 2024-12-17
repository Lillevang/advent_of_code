
data = File.read("./input").strip()
lines = data.split("\n")
line_groups = data.split("\n\n")

lines.each_with_index do |y, row|
    puts "#{y} #{row}"
end