ALPHABET = ('a'..'z').to_a.concat(('A'..'Z').to_a)

def part_1(data : Array(String))
  data.sum do |line|
    p1 = line[0, (line.size/2).to_i32].chars
    p2 = line[(line.size / 2).to_i32, line.size].chars
    common_item = (p1 & p2).first
    ALPHABET.index!(common_item) + 1
  end
end

def part_2(data : Array(String))
  triples = data.each_slice(3)
  triples.sum do |triple|
    t = triple.map(&.chars)
    item = (t[0] & t[1] & t[2]).first
    ALPHABET.index!(item) + 1
  end
end

data = File.read("input").strip().split("\n")
puts part_1(data)
puts part_2(data)
