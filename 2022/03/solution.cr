PRIORITY_MAP = {
  'a' => 1,
  'b' => 2,
  'c' => 3,
  'd' => 4,
  'e' => 5,
  'f' => 6,
  'g' => 7,
  'h' => 8,
  'i' => 9,
  'j' => 10,
  'k' => 11,
  'l' => 12,
  'm' => 13,
  'n' => 14,
  'o' => 15,
  'p' => 16,
  'q' => 17,
  'r' => 18,
  's' => 19,
  't' => 20,
  'u' => 21,
  'v' => 22,
  'w' => 23,
  'x' => 24,
  'y' => 25,
  'z' => 26
}

def priority_value(c : Char)
  c.ascii_uppercase? ? PRIORITY_MAP[c.downcase] + 26 : PRIORITY_MAP[c]
end

def part_1(data : Array(String))
  output = 0
  data.each do |line|
    p1 = line.strip()[0, (line.size/2).to_i32].chars
    p2 = line.strip()[(line.size / 2).to_i32, line.size].chars
    common_item = (p1 & p2).first
    output += priority_value(common_item)
  end
  output
end

def part_2(data : Array(String))
  output = 0
  data.each_slice(3) do |group|
    g1 = group[0].chars
    g2 = group[1].chars
    g3 = group[2].chars
    item = (g1 & g2 & g3).first
    output += priority_value(item)
  end
  output
end

data = File.read("input").strip().split("\n")
puts part_1(data)
puts part_2(data)
