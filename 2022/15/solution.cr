



struct Pos
  property x : Int32
  property y : Int32

  def initialize(@x : Int32, @y : Int32)
  end

end

struct Detection

  property sensor : Pos
  property beacon : Pos

  def initialize(@sensor : Pos, @beacon : Pos)
  end
end


def parse(lines : Array(String))
  detections = Set(Detection).new
  lines.each do |line|
    words = line.split()
    sx = words[2][2...-1].to_i
    sy = words[3][2...-1].to_i
    bx = words[8][2...-1].to_i
    by = words[9][2..-1].to_i
    detections << Detection.new(Pos.new(sx, sy), Pos.new(bx, by))
  end
  detections
end

def part_one()

end


lines = File.read("./input").strip().split("\n")
x = parse(lines)
puts x
