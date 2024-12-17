
data = File.read("./input").strip().split("\n")

walls = Set(Tuple(Int32, Int32)).new # Lets make structs instead when refactoring...
max_y = 0

data.each do |wall|
  wall = wall.split(" -> ")
  (1..wall.size) do |i|
    x,y = wall[i].split(",").map(&.to_i)
