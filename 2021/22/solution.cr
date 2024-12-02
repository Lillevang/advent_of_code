lines = File.read("./input").split("\n")

def get_command(line : String)
  oo, coords = line.split
  m = /x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)/.match(coords).not_nil!.captures
  {oo == "on", m.map { |d| d.not_nil!.to_i }}
end


def part_one(commands : Array(Tuple(Bool, Array(Int32))))
  on = Set(Tuple(Int32, Int32, Int32)).new
  commands.each { |command|
    is_on = command[0]
    x1, x2, y1, y2, z1, z2 = command[1]
    (Math.max(-50, x1)..Math.min(51, x2)).each { |x|
      (Math.max(-50, y1)..Math.min(51, y2)).each { |y|
        (Math.max(-50, z1)..Math.min(51, z2)).each { |z|
          coords = Tuple(Int32, Int32, Int32).new(x, y, z)
          if is_on
            on.add(coords)
          else
            on.delete(coords)
          end
        }
      }
    }
  }
  on
end

def is_valid?(r11 : Int32, r12 : Int32, r21 : Int32, r22 : Int32) : Bool
    r12 >= r11 && r22 >= r21
end

def intersect_ranges(r11 : Int32, r12 : Int32, r21 : Int32, r22 : Int32) : (Array(Int32) | Nil)
    if is_valid?(r11, r12, r21, r22)
        if r21 > r12 || r11 > r22
            return
        end
        nums = [r11, r12, r21, r22].sort
        return [nums[1], nums[2]]
    end
end

def intersect_bounds(bounds_1 : Array(Int32), bounds_2 : Array(Int32)) : (Array(Int32) | Nil)
    x11, x12, y11, y12, z11, z12 = bounds_1
    x21, x22, y21, y22, z21, z22 = bounds_2
    x = intersect_ranges(x11, x12, x21, x22)
    y = intersect_ranges(y11, y12, y21, y22)
    z = intersect_ranges(z11, z12, z21, z22)
    if x.nil? || y.nil? || z.nil?
        return
    end
    return x + y + z
end

class Cuboid

    def initialize(bounds : Array(Int32))
        @bounds = bounds
        @vacuums = Array(Cuboid).new
    end

    def remove(bounds : Array(Int32))
        shaved_bounds = intersect_bounds(@bounds, bounds)
        if !shaved_bounds.nil?
            @vacuums.each { |vacuum|
                vacuum.remove(shaved_bounds)
                
            }
        end
        if !shaved_bounds.nil?
            @vacuums << Cuboid.new(shaved_bounds)
        end
    end

    def volume : Int64
        x1, x2, y1, y2, z1, z2 = @bounds
        _sum = @vacuums.reduce(0.to_i64) { |acc, vacuum| acc + vacuum.volume }
        return (x2 - x1 + 1).to_i64 * (y2 - y1 + 1).to_i64 * (z2 - z1 + 1).to_i64 - _sum
    end
end


def part_two(commands : Array(Tuple(Bool, Array(Int32)))) : Int64
  cuboids = Array(Cuboid).new
  commands.each { |command|
      is_on = command[0]
      bounds = command[1]
      cuboids.each { |cuboid|
          cuboid.remove(bounds)
      }
      if is_on
          cuboids << Cuboid.new(bounds)
      end
  }
  cuboids.reduce(0.to_i64) { |acc, cuboid| acc + cuboid.volume }
end

commands = lines.map { |line| get_command(line) }
p part_one(commands).not_nil!.size
p part_two(commands)