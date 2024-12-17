trees = File.read("./input")
            .strip()
            .split("\n")
            .map(&.each_char.map { |ch| ch.ord - '0'.ord}.to_a ).to_a

raise "bad grid" if trees.size == 0 || trees[1..].any? { |row| row.size != trees[0].size }

visible, max_scene_score = 0, 0
range_x, range_y = 0..(trees[0].size-1), 0..(trees.size-1)
(1...range_y.end).each do |y|
  (1...range_x.end).each do |x|
    is_visible, scene_score = false, 1
    [ {0,1}, {1,0}, {0,-1}, {-1,0} ].each do |dx, dy|
      distance = 0
      ix, iy = x+dx, y+dy
      while range_x.includes?(ix) && range_y.includes?(iy)
        distance += 1
        break if trees[iy][ix] >= trees[y][x]
        ix += dx; iy += dy
      end
      scene_score *= distance
      is_visible ||= !range_x.includes?(ix) || !range_y.includes?(iy)
    end
    visible += is_visible ? 1 : 0
    max_scene_score = [max_scene_score, scene_score].max
  end
end

puts "Part 1:"
puts visible + trees[0].size * 2 + (trees.size - 2) * 2

puts "Part 2:"
puts max_scene_score
