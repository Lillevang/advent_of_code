data = File.read("./input").split("\n")

points = {
    "A X" => {4, 3},
    "A Y" => {8, 4},
    "A Z" => {3, 8},
    "B X" => {1, 1},
    "B Y" => {5, 5},
    "B Z" => {9, 9},
    "C X" => {7, 2},
    "C Y" => {2, 6},
    "C Z" => {6, 7},
    "" => {0,0}
}

p1_score = 0
p2_score = 0

data.each do |x|
    p1_score += points[x][0]
    p2_score += points[x][1]
end

puts "Part one: #{p1_score}"
puts "Part two: #{p2_score}"
