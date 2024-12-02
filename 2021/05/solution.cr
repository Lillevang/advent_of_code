data = File.read_lines("./input")

lines = Array(Array(NamedTuple(x: Int32, y: Int32))).new
data.each do |l|
    pts = l.split(" -> ")
    _l = pts.first.split(",")
    left = {"x": _l.first.to_i, "y": _l.last.to_i}
    _r = pts.last.split(",")
    right = {"x": _r.first.to_i, "y": _r.last.to_i}
    lines << [left, right]
end

coords = Hash(NamedTuple(x: Int32, y: Int32), Int32).new
def mark(coords, x, y)
    coords[{"x": x, "y": y}] = coords.fetch({"x": x, "y": y}, 0) + 1
end


lines.each do |line|
    x1 = line.first[:x]
    y1 = line.first[:y]
    x2 = line.last[:x]
    y2 = line.last[:y]

    if x1 == x2
        ([y1, y2].min..[y1,y2].max).step(1) do |i|
            mark(coords, x1, i)
        end
    elsif y1 == y2
        ([x1, x2].min..[x1, x2].max).step(1) do |i|
            mark(coords, i, y1)
        end
    end
end

p coords.values.count { |i| i > 1 }