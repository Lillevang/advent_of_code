def get_content
  File.read("input").split("\n\n")
end

def get_points(content : Array(String))
  points = Array(Array(Int32)).new
  content[0].split("\n").each {|line|
    points << line.split(",").map &.to_i
  }
  points
end

def get_folds(content : Array(String))
  folds = [] of Int32
  content[1].split("\n").each { |line|
    c = line.split(" ")[2].split("=")[0] == "x" ? 0 : 1
    folds << c
  }
  folds
end

def get_dimensions(points : Array(Array(Int32)))
  max_x = points.flat_map { |p|  p[0] }.max + 1
  max_y = points.flat_map { |p|  p[1] }.max + 1
  [max_x, max_y]
end

def fold(dimensions : Array(Int32), fold : Int32, points : Array(Array(Int32)))
  dimensions[fold] = (dimensions[fold] / 2).to_i
  (0..points.size - 1).each { |p|
    if points[p][fold] > dimensions[fold]
      points[p][fold] -= (points[p][fold] - dimensions[fold]) * 2
    end
  }  
  points
end

def part_one
  content = get_content()
  points = get_points(content)
  folds = get_folds(content)
  dimensions = get_dimensions(points)
  p fold(dimensions, folds[0], points).flat_map { |p| p[1] * dimensions[0] + p[0] }.to_set.size
end

def part_two
  content = get_content()
  points = get_points(content)
  folds = get_folds(content)
  dimensions = get_dimensions(points)
  folds.each { |fold| 
    points = fold(dimensions, fold, points)
  }
  grid = (0..dimensions[0] * dimensions[1]).map {|_| 0}
  points.each { |p|
    grid[p[1] * dimensions[0] + p[0]] = 1
  }
  (0..dimensions[1] - 1).each {|i|
    p grid[i * dimensions[0]..((i + 1) * dimensions[0]) - 1].map { |p| p > 0 ? "#" : " " } .join("")
  }
end

part_one
part_two

